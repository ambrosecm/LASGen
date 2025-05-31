import os
import re
import generateInitSeed
import llm_generate
from concurrent.futures import ThreadPoolExecutor,as_completed
from tqdm import tqdm
import networkx as nx
import shutil
import stat
from datetime import datetime
import proxysetting
from util import *

# afl-fuzz time limit
hour=proxysetting.hour

# Check for crashes and clean up and organize the output folder.
def check_and_clean(inputdir, outputdir, program, harness_code_file,crashes_output_dir):
    crashes_dir = os.path.join(outputdir, "default", "crashes")
    
    # Check whether the crash directory exists and is not empty.
    has_crash_files = False
    if os.path.exists(crashes_dir):
        # Iterate through all subdirectories to check actual files (skip empty directories)
        for root, dirs, files in os.walk(crashes_dir):
            if files:  # Immediately terminate checking when any file is found.
                has_crash_files = True
                break
    # If no crash files are found, clean up the output directory.
    if not has_crash_files:
        try:
            if os.path.exists(outputdir):
                # Define error handling functions for deletion (solve read-only file/permission issues)
                def _force_remove(func, path, exc_info):
                    os.chmod(path, stat.S_IWRITE)  
                    func(path)  

                shutil.rmtree(outputdir, onerror=_force_remove)
                print(f"[+] Output directory cleared: {outputdir}")
            else:
                print(f"[-] The output directory does not exist: {outputdir}")
        except Exception as e:
            print(f"[!] Deletion failed: {str(e)}")
    else:
        print(f"[*] Crash file exists, retain output directory")
        # # Copy crash-related files to crashes_output_dir
        safe_copy(inputdir, crashes_output_dir)
        safe_copy(outputdir, crashes_output_dir)
        safe_copy(program, crashes_output_dir)
        safe_copy(harness_code_file, crashes_output_dir)

def run_afl(fuzz_id, inputdir, outputdir, program, harness_code_file,crashes_dir):
    afl_timeout=3600*hour
    tmp_dir = os.path.join(outputdir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)  

    afl_cmd = [
        "afl-fuzz",
        # "-Q",  
        "-m", "none",  
        "-t", "5000",  
        "-i", inputdir,
        "-o", outputdir,
        "--", program,
        "@@"
    ]
    t,r=execute_command(afl_cmd,timeout=afl_timeout,tmp_dir=tmp_dir,flag=1)
    print(f"Starting AFL instance {fuzz_id} for {program}...")  

    if t:
        print(f"AFL instance {fuzz_id} for {program} timed out. AFL instance successfully completed!")
    else:
        print(f"AFL instance {fuzz_id} failed to run\n")
        print(f"Error output:\n{r or 'No error message'}")
    
    # Check for crashes and clean up and organize the output folder.
    check_and_clean(inputdir, outputdir, program, harness_code_file,crashes_dir)


def find_file_by_symbol(parsed_functions, target_symbol):
    for entry in parsed_functions:
        if entry["symbol"] == target_symbol:
            return entry["file"]
    return None

def prepare_folder(slice_result_base_directory,output_base_directory):
    create_folder(slice_result_base_directory+"/bitcode")
    create_folder(slice_result_base_directory+"/sliced_code")
    create_folder(output_base_directory+"/harness/bitcode")
    create_folder(output_base_directory+"/harness/code")
    create_folder(output_base_directory+"/harness/program")
    create_folder(output_base_directory+"/init_seed")
    create_folder(output_base_directory+"/crashes")
    return

def merge_markdown_files(source_dir, output_file):
    """
    Merge all Markdown files (supports multiple extensions) in the directory into a single output file.
    
    Args:
        source_dir (str): The root directory to search for Markdown files.
        output_file (str): The path of the merged output file.
    """
    markdown_extensions = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn', '.rmd', '.qmd'}

    with open(output_file, 'w', encoding='utf-8',errors='ignore') as outfile:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in markdown_extensions):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8',errors='ignore') as infile:
                        outfile.write(f"# {file}\n\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n---\n\n")  
    
    content=""
    with open(output_file, 'r',errors='ignore') as file:
        content = file.read()

    if not content:
        with open(output_file, 'w',errors='ignore') as file:
            file.write('null')
        return None

    print(f"All Markdown files have been merged into {output_file}")
    return output_file

def find_function_in_ir(ir_file_path, function_name):
    """
    Search for function name modifications in LLVM IR files.
    
    Args:
        ir_file_path (str): Path to the IR file.
        function_name (str): Original function name to search for.

    Returns:
        str: Modified function name (if found), or original function name (if not modified).
    """
    try:
        with open(ir_file_path, 'r', encoding='utf-8',errors='ignore') as file:
            ir_data = file.readlines()
        pattern = rf'distinct !DISubprogram\(name: "{function_name}"(?:, linkageName: "([^"]+)")?'
        for line in ir_data:
            match = re.search(pattern, line)
            if match:
                if match.group(1):
                    return match.group(1)
                else:
                    return function_name
        return function_name

    except FileNotFoundError:
        print( f"The file {ir_file_path} does not exist.")
        return function_name
    except Exception as e:
        print( f"Error occurred: {e}")
        return function_name

# Replace compiler
def replace_compiler(compile_command):
    parts = compile_command.strip().split()
    if not parts:
        return compile_command  
    original_compiler = parts[0]
    compiler_basename = os.path.basename(original_compiler).lower()
    is_cpp = any(key in compiler_basename for key in ("++", "c++", "g++", "clang++"))
    afl_compiler = "afl-clang-fast++" if is_cpp else "afl-clang-fast"
    parts[0] = afl_compiler
    return " ".join(parts)

# Generate complete compilation commands
def get_harness_compile_cmd(command, input_file, output_file, libfile_path,LD_lib_path,headers,file_chain):
    print('=========Obtain compilation commands=========')
    if libfile_path in file_chain:
        file_chain.remove(libfile_path)

    fileheader_path=os.path.dirname(libfile_path)

    # Replace the compiler with afl-clang-fast
    command = replace_compiler(command)
    # Command to switch to clang syntax
    command=sanitize_clang_command(command)
    # Split the command into a list separated by spaces.
    command_parts = command.split()
    command_parts = [part for part in command_parts if part != "-c"]

    # Find and update the output file 
    for i, part in enumerate(command_parts):
        if part == "-o" and i + 1 < len(command_parts):
            command_parts[i + 1] = output_file  
    for i in range(len(command_parts) - 1, -1, -1):
        if not command_parts[i].startswith('-'):
            command_parts[i] = input_file  
            break
    linked_libs = identify_ld_libraries(headers)
    updated_command = " ".join(command_parts)+" -g -O0"
    if LD_lib_path=="":
        updated_command1=updated_command2=updated_command+" -I"+fileheader_path+" "+" ".join(file_chain)+" "+linked_libs
    else:
        LD_suf=os.path.splitext(os.path.basename(LD_lib_path))[1]
        updated_command1=updated_command+" -I"+fileheader_path+" "+LD_lib_path+" "+linked_libs
        if ".so" in LD_suf:
            updated_command2=updated_command+" -I"+fileheader_path+" "+LD_lib_path+" "+" ".join(file_chain)+" "+linked_libs
        else:
            updated_command2=updated_command+" -I"+fileheader_path+" "+" ".join(file_chain)+" "+linked_libs
        
    updated_command=[updated_command1,updated_command2]
    return updated_command

def generate_compile_cmd(libfile_path,compile_cmds,input_file,output_file,LD_lib_path,headers,file_chain):
    print('=========Generate compilation commands=========')
    for compile_cmd in compile_cmds:
        if compile_cmd["file_path"]==libfile_path:
            return get_harness_compile_cmd(compile_cmd["command"], input_file, output_file, libfile_path,LD_lib_path,headers,file_chain)
    
    fileheader_path=os.path.dirname(libfile_path)
    file_suf=os.path.splitext(os.path.basename(libfile_path))[1]
    if file_suf==".c" or file_suf==".h":
        # compile_arg="gcc"
        compile_arg="afl-clang-fast"
    elif file_suf==".cpp" or file_suf==".cc" or file_suf==".cxx" or file_suf==".hpp" or file_suf==".hxx" or file_suf==".c++" or file_suf==".h++" or file_suf==".hh":
        # compile_arg="g++"
        compile_arg="afl-clang-fast++"
    else:
        return None
    linked_libs = identify_ld_libraries(headers)
    if libfile_path in file_chain:
        file_chain.remove(libfile_path)
    if LD_lib_path=="":
        updated_command1=compile_arg+" -g -O0 "+input_file+" -o "+output_file+" -I"+fileheader_path+" "+" ".join(file_chain)+" "+linked_libs
    else:
        LD_suf=os.path.splitext(os.path.basename(LD_lib_path))[1]
        updated_command1=compile_arg+" -g -O0 "+input_file+" -o "+output_file+" -I"+fileheader_path+" "+LD_lib_path+" "+linked_libs
        if ".so" in LD_suf:
            updated_command2=compile_arg+" -g -O0 "+input_file+" -o "+output_file+" -I"+fileheader_path+" "+LD_lib_path+" "+" ".join(file_chain)+" "+linked_libs
        else:
            updated_command2=compile_arg+" -g -O0 "+input_file+" -o "+output_file+" -I"+fileheader_path+" "+" ".join(file_chain)+" "+linked_libs
    updated_command=[updated_command1,updated_command2]
    return updated_command

# Determine whether the slice function has reached the slice count limit.
def check_count_for_slice_fun(slice_fun,parsed_functions):
    for func in parsed_functions:
        if func["symbol"] == slice_fun:
            if func["count"] >= 3:
                return False
    return True

# Counting the number of slices for slice functions
def count_for_slice_fun(slice_fun,parsed_functions):
    for func in parsed_functions:
        if func["symbol"] == slice_fun:
            func["count"] += 1


# Use cscope to obtain the call relationship of a function.
def get_called_functions(func_name: str, db_file: str) -> list:
    cmd = [
        "cscope",
        "-d",  
        "-L",  
        f"-2{func_name}",  
        "-f", db_file
    ]
    t,output=execute_command(cmd)
    if not t:
        print("Error running cscope:", output)

    called_funcs = set()
    for line in output.strip().split('\n'):
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 4:
            called_func = (parts[1],parts[0])
            called_funcs.add(called_func)
    return sorted(called_funcs)

# Generate function call graph
def generate_call_graph(parsed_functions,cscope_db_file):
    # Creating a directed graph
    G = nx.DiGraph()
    # [{"symbol": symbol,"file": file_path,"signature": signature,"count": 0}]
    for fun in parsed_functions:
        symbol=fun["symbol"]
        file=fun["file"]
        # 添加节点
        node=(symbol,file)
        G.add_node(node,symbol=symbol,file=file)
        called_functions = get_called_functions(symbol, cscope_db_file)
        for called_symbol, called_file in called_functions:
            c_fun_file=called_file
            index=0
            for f in parsed_functions:
                if f["symbol"] == called_symbol and f["file"] == called_file:
                    index=1
                    break
                if f["symbol"] == called_symbol:
                    c_fun_file=f["file"]
            if index==0:
                called_file=c_fun_file
            called_node = (called_symbol, called_file)
            if not G.has_node(called_node):
                G.add_node(called_node, symbol=called_symbol, file=called_file)
            G.add_edge(node, called_node)
    return G

# Preliminary screening of functions that can be sliced
def extract_slice_funs(libfile_path,parsed_functions):
    slice_funs = []
    function_call_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s*\(', re.MULTILINE)
    try:
        with open(libfile_path, 'r', encoding='utf-8',errors='ignore') as f:
            code = f.read()
        matches = function_call_pattern.findall(code)
        keywords = {"if", "for", "while", "switch", "return", "sizeof", "catch", "throw", "delete", "new","printf","int"}
        slice_funs = [match for match in matches if match not in keywords]
        slice_funs = list(dict.fromkeys(slice_funs))
    except FileNotFoundError:
        print(f"Error: File {libfile_path} not found.")
    except Exception as e:
        print(f"Error: Exception occurred while reading file: {e}")
    
    parsed_symbols = {entry['symbol'] for entry in parsed_functions}
    slice_funs = {fun for fun in slice_funs if fun in parsed_symbols}
    return slice_funs

# Extract the function definition code
def extract_fun_code(fun,bc_file,ll_file,file_path,base_directory):
    fun_code=""
    fun=find_function_in_ir(ll_file, fun)
    create_folder(base_directory+"/tmp")
    tmp_fun_bc_file=base_directory+"/tmp/fun_bc.bc"
    fun_code_file=base_directory+"/"+fun+"_fun.c"

    llvm_extract_cmd="llvm-extract-10 -func="+fun+" "+bc_file+" -o "+tmp_fun_bc_file
    execute_command(llvm_extract_cmd)

    llvm_to_source=os.path.dirname(os.path.abspath(__file__))+"/dg/build/tools/llvm-to-source"
    to_source_code_cmd=llvm_to_source+" "+tmp_fun_bc_file+" "+file_path+" > "+fun_code_file
    execute_command(to_source_code_cmd)

    try:
        with open(fun_code_file, 'r',errors='ignore') as file:
            fun_code = file.read()
    except FileNotFoundError:
        "File not found."
    except Exception as e:
        str(e)

    return fun_code

# Calling function slice
def slice_code(entry_fun,slice_fun,libfile_path,bc_file,ll_file,sliced_code_entry_fun_folder,headers,entry_fun_code):
    sliced_bc_file=sliced_code_entry_fun_folder+"/"+slice_fun+".bc"
    sliced_code_file=sliced_code_entry_fun_folder+"/"+slice_fun+os.path.splitext(os.path.basename(libfile_path))[1]

    ll_entry_fun = find_function_in_ir(ll_file, entry_fun)
    ll_slice_fun = find_function_in_ir(ll_file, slice_fun)
    
    slicer=os.path.dirname(os.path.abspath(__file__))+"/dg/build/tools/llvm-slicer"
    slice_cmd=slicer+" --entry="+ll_entry_fun+" -c "+ll_slice_fun+" "+bc_file+" -o "+sliced_bc_file
    execute_command(slice_cmd)

    llvm_to_source=os.path.dirname(os.path.abspath(__file__))+"/dg/build/tools/llvm-to-source"
    to_source_code_cmd=llvm_to_source+" "+sliced_bc_file+" "+libfile_path+" > "+sliced_code_file
    execute_command(to_source_code_cmd)
    if not os.path.exists(sliced_code_file) or os.path.getsize(sliced_code_file) == 0:
        with open(sliced_code_file, "w", encoding="utf-8",errors='ignore') as file:
            file.write(entry_fun_code)
        
        insert_headers(sliced_code_file,headers)
    else:
        insert_headers(sliced_code_file,headers)

    return sliced_code_file

# Calling function forward slicing
def slice_code_forward(entry_fun,slice_fun,libfile_path,result_main_bc_file,ll_file,sliced_code_entry_fun_folder,file_chain,slice_fun_code):
    print('=========Generate forward slice code=========')
    sliced_bc_forward_file=sliced_code_entry_fun_folder+"/"+slice_fun+"_forward.bc"
    sliced_code_forward_file=sliced_code_entry_fun_folder+"/"+slice_fun+"_forward"+os.path.splitext(os.path.basename(libfile_path))[1]

    ll_entry_fun = find_function_in_ir(ll_file, entry_fun)
    ll_slice_fun = find_function_in_ir(ll_file, slice_fun)

    slicer=os.path.dirname(os.path.abspath(__file__))+"/dg/build/tools/llvm-slicer"
    slice_forward_cmd=slicer+" --forward --entry="+ll_entry_fun+" -c "+ll_slice_fun+" "+result_main_bc_file+" -o "+sliced_bc_forward_file
    execute_command(slice_forward_cmd)
    llvm_to_source=os.path.dirname(os.path.abspath(__file__))+"/dg/build/tools/llvm-to-source"
    sliced_code_forward=""
    for f in file_chain:
        to_source_code_cmd=llvm_to_source+" "+sliced_bc_forward_file+" "+ f
        t,r=execute_command(to_source_code_cmd)
        if t:
            sliced_code_forward=f+":\n"+r+sliced_code_forward
    if sliced_code_forward=="":
        sliced_code_forward=slice_fun_code
    with open(sliced_code_forward_file, 'w', encoding='utf-8',errors='ignore') as file:
        file.write(sliced_code_forward)
    return sliced_code_forward_file


# Get the file list corresponding to the function call chain
def get_file_call_chain_bc(fun_call_graph,libfile_path,slice_fun_libfile_path,compile_cmds,bitcode_directory,slice_fun):
    file_list = []
    for compile_cmd in compile_cmds:
        directory = compile_cmd.get("directory", "")
        file = compile_cmd.get("file", "")
        if directory and file:
            file_list.append(compile_cmd["file_path"])
    
    start_node=(slice_fun,slice_fun_libfile_path)
    print("============start_node：============")
    print(start_node)
    try:
        all_descendants = nx.bfs_tree(fun_call_graph, source=start_node).nodes
        # all_descendants = nx.descendants(fun_call_graph, start_node)
    except nx.NetworkXError:
        all_descendants = set()
    unique_files = set()
    for node in all_descendants:
        if "file" in fun_call_graph.nodes[node] and fun_call_graph.nodes[node]["file"] in file_list:
            unique_files.add(fun_call_graph.nodes[node]["file"])
    print("============Function call chain:============")
    print(all_descendants)
    file_chain=list(unique_files)
    if slice_fun_libfile_path not in file_chain:
        file_chain.append(slice_fun_libfile_path)
    if libfile_path not in file_chain:
        file_chain.append(libfile_path)
    bc_file_chain=[]
    for file in file_chain:
        bc_file_chain.append(bitcode_directory+"/"+os.path.basename(file)+"/"+os.path.splitext(os.path.basename(file))[0]+".bc")
        
    print("============file_chain：============")
    print(file_chain)
    print(bc_file_chain)
    return file_chain,bc_file_chain


def generate_harness(sliced_code_file,slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain):
    print('=========Generate Harness=========')
    file_suf=os.path.splitext(os.path.basename(harness_code_file))[1]
    code_type=""
    if file_suf==".c":
        code_type="C"
    elif file_suf==".cpp" or file_suf==".cc" or file_suf==".cxx":
        code_type="C++"
    with open(sliced_code_file, 'r',errors='ignore') as file:
        sliced_code = file.read()
    # Generate initial driver code
    init_harness,input_prompt=llm_generate.generate_harness(sliced_code,slice_fun,slice_fun_code,code_type,rag_chain)
    # Make sure the folder in the path exists
    os.makedirs(os.path.dirname(harness_code_file), exist_ok=True)
    os.makedirs(os.path.dirname(harness_program_file), exist_ok=True)
    with open(harness_code_file, 'w',errors='ignore') as file:
        file.write(str(init_harness) if init_harness is not None else "")
    with open(harness_code_file+"_cmd.txt", 'w',errors='ignore') as file:
        file.write(harness_compile_cmd[0]+'\n\n'+harness_compile_cmd[1])
    t0,r0=execute_command(harness_compile_cmd[0])
    if t0:
        return harness_program_file
    t1,r1=execute_command(harness_compile_cmd[1])
    if t1:
        return harness_program_file
    f=0
    re_harness=init_harness
    while not t0:
        f+=1
        if f>=4:
            break
        re_harness=llm_generate.re_generate_harness_with_error(rag_chain,r0,re_harness,input_prompt)
        with open(harness_code_file, 'w',errors='ignore') as file:
            file.write(str(re_harness) if re_harness is not None else "")
        t0,r0=execute_command(harness_compile_cmd[0])
    if t0:
        return harness_program_file
    if harness_compile_cmd[0] == harness_compile_cmd[1]:
        return False
    
    t1,r1=execute_command(harness_compile_cmd[1])
    f=0
    re_harness=init_harness
    while not t1:
        f+=1
        if f>=3:
            with open(harness_program_file, 'w',errors='ignore') as file:
                file.write(str(r1))
            return False
        re_harness=llm_generate.re_generate_harness_with_error(rag_chain,r1,re_harness,input_prompt)
        with open(harness_code_file, 'w',errors='ignore') as file:
            file.write(str(re_harness) if re_harness is not None else "")
        t1,r1=execute_command(harness_compile_cmd[1])
    
    return harness_program_file

def generate_harness_by_KG(slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain,headers):
    print('=========Generate Harness=========')
    file_suf=os.path.splitext(os.path.basename(harness_code_file))[1]
    code_type=""
    if file_suf==".c":
        code_type="C"
    elif file_suf==".cpp" or file_suf==".cc" or file_suf==".cxx":
        code_type="C++"
    init_harness,input_prompt=llm_generate.generate_harness_without_slicecode(slice_fun,slice_fun_code,headers,code_type,rag_chain)
    os.makedirs(os.path.dirname(harness_code_file), exist_ok=True)
    os.makedirs(os.path.dirname(harness_program_file), exist_ok=True)
    with open(harness_code_file, 'w',errors='ignore') as file:
        file.write(str(init_harness) if init_harness is not None else "")
    with open(harness_code_file+"_cmd.txt", 'w',errors='ignore') as file:
        file.write(harness_compile_cmd[0]+'\n\n'+harness_compile_cmd[1])
    t0,r0=execute_command(harness_compile_cmd[0])
    f=0
    re_harness=init_harness
    while not t0:
        f+=1
        if f>=4:
            break
        re_harness=llm_generate.re_generate_harness_with_error(rag_chain,r0,re_harness,input_prompt)
        with open(harness_code_file, 'w',errors='ignore') as file:
            file.write(str(re_harness) if re_harness is not None else "")
        t0,r0=execute_command(harness_compile_cmd[0])

    if t0:
        return harness_program_file
    if harness_compile_cmd[0] == harness_compile_cmd[1]:
        return False

    t1,r1=execute_command(harness_compile_cmd[1])
    f=0
    re_harness=init_harness
    while not t1:
        f+=1
        if f>=3:
            with open(harness_program_file, 'w',errors='ignore') as file:
                file.write(str(r1))
            return False
        re_harness=llm_generate.re_generate_harness_with_error(rag_chain,r1,re_harness,input_prompt)
        with open(harness_code_file, 'w',errors='ignore') as file:
            file.write(str(re_harness) if re_harness is not None else "")
        t1,r1=execute_command(harness_compile_cmd[1])

    return harness_program_file

# Create an output folder and check if the program and seed folders exist. If not, return false.
def create_output_folder(harness_program_file,init_seed_dir_path):
    outputdir=""
    if not os.path.exists(harness_program_file):  
        return False
    if not os.path.exists(init_seed_dir_path):
        return False
    files_and_dirs = os.listdir(init_seed_dir_path)
    if len(files_and_dirs) == 0:
        return False
    parent_dir = os.path.dirname(init_seed_dir_path)  
    outputdir = os.path.join(parent_dir, "output")  
    create_folder(outputdir)  
    return outputdir

# Fuzzing LLM generation with sliced ​​code
def fuzz_with_llm_and_slicecode(sliced_code_file,slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness,sliced_code_forward_file,init_seed_dir,rag_chain_seed,crashes_dir,afl_executor,afl_futures):

    init_seed_dir_path=init_seed_dir+"/input"
    if not os.path.exists(harness_program_file):
        # Generate complete code based on slice code # /output file base path/harness/code/slice file name/entry function name/slice function name
        harness_program_file=generate_harness(sliced_code_file,slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness)
        if not harness_program_file:
            print("==========Failed to generate harness executable, skipping fuzzing stage===========")
            return

    #Generate initial seed
    if not os.path.exists(init_seed_dir_path):
        # Generate a seed file and return the folder path of the generated seed file # /output file base path/init_seed/slice file name/entry function name/slice function name/input
        init_seed_dir_path=generateInitSeed.generate_init_seed_by_LLM(sliced_code_forward_file,harness_code_file,slice_fun,slice_fun_code,init_seed_dir,harness_program_file,rag_chain_seed)
    outputdir=create_output_folder(harness_program_file,init_seed_dir_path)
    if not outputdir:
        return
    if os.path.isdir(outputdir+"/default/crashes"):
        print("==========Fuzz results already exist, no need to fuzz again=============")
        return
    # Submit AFL execution tasks to the thread pool
    afl_futures.append(afl_executor.submit(run_afl, slice_fun, init_seed_dir_path, outputdir, harness_program_file,harness_code_file,crashes_dir))
    print(f"{slice_fun} Submitted to AFL!")
    return

# Fuzzing for normal LLM generation
def fuzz_with_llm(slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness,headers,init_seed_dir,rag_chain_seed,crashes_dir,afl_executor,afl_futures):
    
    init_seed_dir_path=init_seed_dir+"/input"
    if not os.path.exists(harness_program_file):
        harness_program_file=generate_harness_by_KG(slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness,headers)
        if not harness_program_file:
            print("==========Failed to generate harness executable, skipping fuzzing stage===========")
            return
    if not os.path.exists(init_seed_dir_path):
        init_seed_dir_path=generateInitSeed.generate_init_seed_by_LLM("",harness_code_file,slice_fun,slice_fun_code,init_seed_dir,harness_program_file,rag_chain_seed)

    outputdir=create_output_folder(harness_program_file,init_seed_dir_path)
    if not outputdir:
        return
    if os.path.isdir(outputdir+"/default/crashes"):
        print("==========Fuzz results already exist, no need to fuzz again=============")
        return
    afl_futures.append(afl_executor.submit(run_afl, slice_fun, init_seed_dir_path, outputdir, harness_program_file,harness_code_file,crashes_dir))
    print(f"{slice_fun} Submitted to AFL!")
    return
    
if __name__ == "__main__":

    lib_id=proxysetting.lib_id
    lib_directory=proxysetting.lib_directory
    compile_cmds_file=proxysetting.compile_cmds_file
    LD_lib_path=proxysetting.LD_lib_path
    vul_fun_list=proxysetting.vul_fun_list


    # Set dynamic library link environment variables
    if LD_lib_path.endswith(".so"):
        LD_lib_dir_path=os.path.dirname(LD_lib_path)
        current_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = f"{LD_lib_dir_path}:{current_ld_path}" if current_ld_path else LD_lib_dir_path

    # Create a tile output folder
    slice_result_base_directory=os.path.dirname(os.path.abspath(__file__))+"/slice_result/"+os.path.basename(lib_directory)+lib_id
    # AFL fuzz testing time unit: h
    hour=24
    # Create harness output folder
    output_base_directory=os.path.dirname(os.path.abspath(__file__))+"/output/"+os.path.basename(lib_directory)+lib_id
    prepare_folder(slice_result_base_directory,output_base_directory)
    # Merge knowledge base file information
    output_md_file = slice_result_base_directory+"/KnowledgeBase.md"    
    flag=merge_markdown_files(lib_directory, output_md_file)
    # Generate document segmentation vectordb
    vectorstoredb=llm_generate.generateVecDB(slice_result_base_directory,flag)
    vectorstoredb=None
    # Generate RAG chain, parameters: document vector folder, llm temperature
    # {"rag_chain": rag_chain,"flag":None}
    rag_chain_harness=llm_generate.generate_RAG_chain_without_history(vectorstoredb,0.6)
    rag_chain_seed=llm_generate.generate_RAG_chain_without_history(vectorstoredb,0.6)
    updated_compile_cmds_file = slice_result_base_directory+'/updated_compile_commands.json'  

    # Process the compile_commands JSON file
    process_compile_commands(compile_cmds_file, updated_compile_cmds_file)
    compile_cmds = read_json_file(updated_compile_cmds_file)
    bitcode_directory=slice_result_base_directory+"/bitcode"
    sliced_code_directory=slice_result_base_directory+"/sliced_code"
    print("=========Compile to bitcode=========")
    for compile_cmd in compile_cmds:
        bitcode_folder=bitcode_directory+"/"+os.path.basename(compile_cmd["file_path"])
        create_folder(bitcode_folder)
        libfile_path=compile_cmd["file_path"]
        modify_main_function(libfile_path)
        bc_file,ll_file=compile_to_bc(compile_cmd,libfile_path,bitcode_folder)
    print("=========Compiling bitcode is finished=========")

    # Generate tags file (containing all function information in the library)
    tag_file=slice_result_base_directory+"/tags"
    generate_tags(tag_file,lib_directory)
    parsed_functions = parse_tags(tag_file)

    # Generate function call relation database
    cscope_db_file=slice_result_base_directory+"/cscope.out"
    t,cscope_files=generate_cscope_db(lib_directory, cscope_db_file)
    if not t:
        raise
    # Generate a function call graph for a library
    fun_call_graph=generate_call_graph(parsed_functions,cscope_db_file)

    # Set the maximum thread pool size (number of concurrently executing LLM instances)
    llm_max_threads = proxysetting.llm_max_threads
    # Set the maximum thread pool size (number of concurrently executing AFL instances)
    afl_max_threads = proxysetting.afl_max_threads

    # Create a thread pool to execute AFL asynchronously
    with ThreadPoolExecutor(max_workers=llm_max_threads) as llm_executor,ThreadPoolExecutor(max_workers=afl_max_threads) as afl_executor:
        llm_futures = []  
        afl_futures = []  
        for compile_cmd in compile_cmds:
            bitcode_folder=bitcode_directory+"/"+os.path.basename(compile_cmd["file_path"])
            sliced_code_folder=sliced_code_directory+"/"+os.path.basename(compile_cmd["file_path"])
            create_folder(sliced_code_folder)
            libfile_path=compile_cmd["file_path"]
            print("=========The slice target file is=========")
            print(libfile_path)
            complete_headers,headers = extract_headers(libfile_path)
            slice_funs=extract_slice_funs(libfile_path,parsed_functions)
            print("=========List of functions that can slice=========")
            print(slice_funs)
            entry_funs=extract_entry_funs(libfile_path)
            print("=========Slice entry function=========")
            print(entry_funs)
            bc_file=bitcode_folder+"/"+os.path.splitext(os.path.basename(libfile_path))[0]+".bc"
            ll_file=bitcode_folder+"/"+os.path.splitext(os.path.basename(libfile_path))[0]+".ll"

            for entry_fun in entry_funs:
                sliced_code_entry_fun_folder=sliced_code_folder+"/"+entry_fun
                create_folder(sliced_code_entry_fun_folder)
                entry_fun_code=extract_fun_code(entry_fun,bc_file,ll_file,libfile_path,sliced_code_entry_fun_folder)
                for slice_fun in slice_funs:
                    if vul_fun_list is not None and slice_fun not in vul_fun_list:
                        continue
                    if re.findall(rf'\b{slice_fun}\b', entry_fun_code) and slice_fun!=entry_fun:
                        rec=check_count_for_slice_fun(slice_fun,parsed_functions)
                        if not rec:
                            continue
                        slice_fun_libfile_path=find_file_by_symbol(parsed_functions, slice_fun)
                        slice_fun_bc_file=bitcode_directory+"/"+os.path.basename(slice_fun_libfile_path)+"/"+os.path.splitext(os.path.basename(slice_fun_libfile_path))[0]+".bc"
                        slice_fun_ll_file=bitcode_directory+"/"+os.path.basename(slice_fun_libfile_path)+"/"+os.path.splitext(os.path.basename(slice_fun_libfile_path))[0]+".ll"
                        slice_fun_sliced_code_folder=sliced_code_entry_fun_folder
                        slice_fun_code=extract_fun_code(slice_fun,slice_fun_bc_file,slice_fun_ll_file,slice_fun_libfile_path,slice_fun_sliced_code_folder)
                        sliced_code_file=slice_code(entry_fun,slice_fun,libfile_path,bc_file,ll_file,sliced_code_entry_fun_folder,complete_headers,entry_fun_code)
                        harness_code_file=output_base_directory+"/harness/code/"+os.path.basename(libfile_path)+"/"+entry_fun+"/"+slice_fun+os.path.splitext(os.path.basename(libfile_path))[1]
                        harness_program_file=output_base_directory+"/harness/program/"+os.path.basename(libfile_path)+"/"+entry_fun+"/"+slice_fun
                        header_file_chain=get_header_chain_bc(cscope_files,libfile_path)
                        harness_compile_cmd=get_harness_compile_cmd(compile_cmd["command"],harness_code_file,harness_program_file,libfile_path,LD_lib_path,headers,header_file_chain)
                        print("=========harness_compile_cmd=========")
                        print(harness_compile_cmd)

                        #Code forward slicing
                        file_chain,bc_file_chain=get_file_call_chain_bc(fun_call_graph,libfile_path,slice_fun_libfile_path,compile_cmds,bitcode_directory,slice_fun)
                        result_main_bc_file=bitcode_folder+"/"+entry_fun+"_"+slice_fun+"_link_result.bc"
                        result_main_bc_file=llvm_link_bc(bc_file_chain,result_main_bc_file,bc_file,slice_fun_bc_file)
                        sliced_code_forward_file=slice_code_forward(entry_fun,slice_fun,libfile_path,result_main_bc_file,ll_file,sliced_code_entry_fun_folder,file_chain,slice_fun_code)
                        init_seed_dir=output_base_directory+"/init_seed/"+os.path.basename(libfile_path)+"/"+entry_fun+"/"+slice_fun

                        # Slice function count
                        count_for_slice_fun(slice_fun,parsed_functions)
                        crashes_dir=output_base_directory+"/crashes/"+os.path.basename(libfile_path)+"/"+entry_fun+"/"+slice_fun
                        # Submit LLM execution tasks to the thread pool
                        llm_futures.append(llm_executor.submit(fuzz_with_llm_and_slicecode, sliced_code_file,slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness,sliced_code_forward_file,init_seed_dir,rag_chain_seed,crashes_dir,afl_executor,afl_futures))
       
        print('=========Start the slicing-free code generation harness and seed process=========')
        for fun_intem in parsed_functions:
            if fun_intem["count"] == 0:
                slice_fun=fun_intem["symbol"]
                libfile_path=fun_intem["file"]
                if vul_fun_list is not None and slice_fun not in vul_fun_list:
                    continue
                slice_fun_sliced_code_folder=sliced_code_directory+"/"+os.path.basename(libfile_path)
                create_folder(slice_fun_sliced_code_folder)
                bc_file=bitcode_directory+"/"+os.path.basename(libfile_path)+"/"+os.path.splitext(os.path.basename(libfile_path))[0]+".bc"
                ll_file=bitcode_directory+"/"+os.path.basename(libfile_path)+"/"+os.path.splitext(os.path.basename(libfile_path))[0]+".ll"
                slice_fun_code=""
                if os.path.exists(bc_file) and os.path.exists(ll_file):
                    slice_fun_code=extract_fun_code(slice_fun,bc_file,ll_file,libfile_path,slice_fun_sliced_code_folder)
                
                file_suf=suf=os.path.splitext(os.path.basename(libfile_path))[1]
                if file_suf==".c" or file_suf==".h":
                    suf=".c"
                elif file_suf==".cpp" or file_suf==".cc" or file_suf==".cxx" or file_suf==".hpp" or file_suf==".hxx" or file_suf==".c++" or file_suf==".h++" or file_suf==".hh":
                    suf=".cpp"
                harness_code_file=output_base_directory+"/harness/code/"+os.path.basename(libfile_path)+"/generate/"+slice_fun+suf
                harness_program_file=output_base_directory+"/harness/program/"+os.path.basename(libfile_path)+"/generate/"+slice_fun
                complete_headers,headers = extract_headers(libfile_path)
                
                header_file_chain=get_header_chain_bc(cscope_files,libfile_path)
                harness_compile_cmd=generate_compile_cmd(libfile_path,compile_cmds,harness_code_file,harness_program_file,LD_lib_path,headers,header_file_chain)
                print("=========harness_compile_cmd=========")
                print(harness_compile_cmd)
                if not harness_compile_cmd:
                    continue
                # LLM generates initial seeds
                init_seed_dir=output_base_directory+"/init_seed/"+os.path.basename(libfile_path)+"/generate/"+slice_fun
                crashes_dir=output_base_directory+"/crashes/"+os.path.basename(libfile_path)+"/generate/"+slice_fun

                # Submit LLM execution tasks to the thread pool
                llm_futures.append(llm_executor.submit(fuzz_with_llm, slice_fun,slice_fun_code,harness_compile_cmd,harness_code_file,harness_program_file,rag_chain_harness,complete_headers,init_seed_dir,rag_chain_seed,crashes_dir,afl_executor,afl_futures))
 
        with open(output_base_directory+"/parsed_functions.txt", 'w',errors='ignore') as file:
            file.write(str(parsed_functions))

        for future in tqdm(as_completed(llm_futures), total=len(llm_futures), desc="LLM Gen Processing"):
            result = future.result()

        for future in tqdm(as_completed(afl_futures), total=len(afl_futures), desc="AFL FUZZ Processing"):
            result = future.result()