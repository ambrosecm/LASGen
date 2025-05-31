import subprocess
import os
import shlex
import shutil
import json
import re
from pathlib import Path
import queue

def execute_command(command,timeout=600,tmp_dir=os.getcwd(),flag=0):
    def safe_decode(data):
        if isinstance(data, bytes):
            return data.decode('utf-8', errors='replace')
        return data
    if isinstance(command, list):
        command = ' '.join(map(shlex.quote, command))  
    elif not isinstance(command, str):
        return False, "Invalid command type"

    print("Executing command:", command)
    proc = None
    try:
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors='ignore',
            universal_newlines=True,
            encoding='utf-8',
            cwd=tmp_dir,
            env=os.environ.copy()  
        )
        
        stdout, stderr = proc.communicate(timeout=timeout)

        stderr = safe_decode(stderr).strip()
        stdout = safe_decode(stdout).strip()

        if proc.returncode != 0:
            raise subprocess.CalledProcessError(
                proc.returncode, command, output=stdout, stderr=stderr
            )
            
        print("Command executed successfully.")
        return True, stdout
        
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {str(timeout)} minutes.")
        if proc:
            proc.terminate()
            try:
                proc.wait(2)  
            except subprocess.TimeoutExpired:
                proc.kill()
        if flag==1:
            return True, f"Command timed out after {str(timeout)} minutes."
        return False, f"Command timed out after {str(timeout)} minutes."
        
    except subprocess.CalledProcessError as e:
        stderr = safe_decode(e.stderr).strip()
        print("Error while executing command:")
        print(stderr)
        return False, stderr
        
    except Exception as e:
        return False, str(e)
    except: pass
    finally:
        if proc:
            if proc.stdout: proc.stdout.close()
            if proc.stderr: proc.stderr.close()
            if proc.poll() is None: 
                try: proc.kill()
                except: pass
    return False, "Unknown error" 


def copy_to_directory(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, os.path.basename(src))
    shutil.copy2(src, dst_path)
    return dst_path

def copy_directory(src_dir, dst_dir):
    os.makedirs(os.path.dirname(dst_dir), exist_ok=True)
    shutil.copytree(src_dir, dst_dir)
    return dst_dir

def safe_copy(src, dst_dir):
    try:
        if not os.path.exists(src):
            raise FileNotFoundError(f"The source path does not exist:{src}")
            
        if os.path.isfile(src):
            return copy_to_directory(src, dst_dir)
        else:
            dst_path = os.path.join(dst_dir, os.path.basename(src))
            return copy_directory(src, dst_path)
            
    except (shutil.Error, PermissionError) as e:
        print(f"Copy Failure: {str(e)}")
        return None
    except Exception as e:
        print(f"Unknown error: {str(e)}")
        return None

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"The folder '{folder_path}' has been created or already exists.")
        return True
    except Exception as e:
        print(f"An error occurred while creating folder '{folder_path}': {e}")
        return False

def identify_ld_libraries(headers):
    header_to_library = {
        "math.h": "-lm",
        "cmath": "-lm",
        "thread": "-pthread",
        "mutex": "-pthread",
        "pthread.h": "-pthread",

        "jpeglib.h": "-ljpeg",  
        "png.h": "-lpng",      
        "zlib.h": "-lz",
        "tiffio.h": "-ltiff",
        "webp/encode.h": "-lwebp",
        "gif_lib.h": "-lgif",

        "curl/curl.h": "-lcurl",
        "openssl/ssl.h": "-lssl -lcrypto",
        "gnutls/gnutls.h": "-lgnutls",
        "libssh2.h": "-lssh2",
        "libpq-fe.h": "-lpq",
        "libmongoc/mongoc.h": "-lmongoc-1.0",
        "libmongoc/mongoc-client.h": "-lmongoc-1.0",
        "pcap.h": "-lpcap",

        "sqlite3.h": "-lsqlite3",
        "mysql/mysql.h": "-lmysqlclient",
        "pq-fe.h": "-lpq",
        "SDL/SDL.h": "-lSDL",
        "SDL2/SDL.h": "-lSDL2",
        "GL/gl.h": "-lGL",
        "GL/glew.h": "-lGLEW",
        "GLFW/glfw3.h": "-lglfw",
        "GLUT/glut.h": "-lglut",
        "SFML/Graphics.hpp": "-lsfml-graphics",
        "SFML/Audio.hpp": "-lsfml-audio",
        "SFML/Network.hpp": "-lsfml-network",
        "SFML/System.hpp": "-lsfml-system",

        "freetype/freetype.h": "-lfreetype",
        "harfbuzz/hb.h": "-lharfbuzz",
        "cairo.h": "-lcairo",
        "pango/pango.h": "-lpango-1.0",

        "gsl/gsl_math.h": "-lgsl -lgslcblas",
        "mpg123.h": "-lmpg123",
        "ao/ao.h": "-lao",
        "portaudio.h": "-lportaudio",
        "sndfile.h": "-lsndfile",
        "fftw3.h": "-lfftw3",
        "opencv2/opencv.hpp": "-lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_imgcodecs",
        "opencv2/core.hpp": "-lopencv_core",
        "opencv2/highgui.hpp": "-lopencv_highgui",
        "opencv2/imgproc.hpp": "-lopencv_imgproc",

        "json-c/json.h": "-ljson-c",
        "yaml.h": "-lyaml",
        "libxml/parser.h": "-lxml2",
        "libxslt/xslt.h": "-lxslt",
        "libxslt/xsltInternals.h": "-lxslt",
        "libxslt/xsltutils.h": "-lxslt",
        "libxml/xmlmemory.h": "-lxml2",
    }
    # Collect the libraries that need to be linked
    linked_libraries = set()
    for header in headers:
        library = header_to_library.get(header)
        if library:
            linked_libraries.add(library)
    return " ".join(sorted(linked_libraries))

def read_json_file(file_path):
    with open(file_path, 'r',errors='ignore') as f:
        return json.load(f)

def write_json_file(file_path, data):
    with open(file_path, 'w',errors='ignore') as f:
        json.dump(data, f, indent=4)

def extract_headers(file_path):
    complete_headers = set()
    include_pattern = re.compile(
        r'^\s*#include\s*(<[^>]+>|"[^"]+")\s*?(?:/\*.*?\*/)?\s*?$'  
    )
    if os.path.exists(file_path):
        with open(file_path, 'r', errors='ignore') as f:
            for line in f:
                line = line.split('//')[0].strip()  
                match = include_pattern.match(line)
                if match:
                    complete_headers.add(f"#include {match.group(1)}")

    header_extensions = ['.h', '.hpp', '.hxx', '.hh', '.h++', '.c', '.cpp', '.cc', '.cxx', '.c++']
    base_name = os.path.splitext(file_path)[0]
    for ext in header_extensions:
        header_file = f"{base_name}{ext}"
        
        if os.path.exists(header_file):
            try:
                with open(header_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.split('//')[0].strip()
                        match = include_pattern.match(line)
                        if match:
                            complete_headers.add(f"#include {match.group(1)}")
            except IOError as e:
                print(f"Unable to read header file {header_file}: {str(e)}")
            except Exception as e:
                print(f"An error occurred while processing header file {header_file}: {str(e)}")
    complete_headers.add("#include \""+os.path.basename(file_path)+"\"")
    complete_headers = list(complete_headers)  
    pattern = r'#include\s*[<"](.*?)[>"]'
    headers=list({re.search(pattern, header).group(1) for header in complete_headers})
    return complete_headers,headers 

def get_header_chain_bc(cscope_files,libfile_path):
    file_chain=[]
    file_list = []
    try:
        with open(cscope_files, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    file_list.append(cleaned_line)
    except FileNotFoundError:
        print(f"Error: file {cscope_files} does not exist")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
    
    queue_l=queue.Queue()
    processed_files = set()  
    queue_l.put(libfile_path)
    while not queue_l.empty():
        file=queue_l.get()
        if file in processed_files:  
            continue
        processed_files.add(file)
        complete_headers,headers=extract_headers(file)
        for header in headers:
            for file in file_list:
                if os.path.basename(file) == os.path.basename(header):
                    if file not in file_chain:
                        file_chain.append(file)
                        queue_l.put(file)
    ext_pairs = ['.h', '.hpp', '.hxx', '.hh', '.h++']
    c_ext_pairs = ['.c', '.cpp', '.cc', '.cxx', '.c++']
    filtered_files = set()
    for path in file_chain:
        base, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ext_pairs:
            continue 
        for paired_ext in c_ext_pairs:
            paired_file = f"{base}{paired_ext}"
            if os.path.exists(paired_file):
                filtered_files.add(paired_file)
    file_chain=list(filtered_files)
    if libfile_path not in file_chain:
        file_chain.append(libfile_path)
    print("============Header file call chain: ============")
    print(file_chain)
    return file_chain

# Run the ctags command to generate tags file
def generate_tags(tag_file,input_directory):
    cmd=['ctags', '-R','--languages=c,c++','--c-kinds=f', '--c++-kinds=f','--fields=S','--exclude=tests', '--exclude=demo', '-f',tag_file,input_directory]
    t,output=execute_command(cmd,timeout=1800)
    if t:
        print("Tags file generated successfully.")
    else:
        print("Error running ctags:", output)


# Parse the tags file and return the parsed data
def parse_tags(file_path):
    """
    Parse a ctags file and return structured information for functions only.

    Args:
        file_path (str): Path to the ctags file.

    Returns:
        list[dict]: List of dictionaries containing parsed information.
    """
    parsed_data = []
    with open(file_path, 'r',errors='ignore') as f:
        for line in f:
            # Skip metadata lines starting with '!'
            if line.startswith('!'):
                continue

            # Skip empty lines or lines not in the expected format
            if not line.strip():
                continue

            try:
                # Split the line by tab characters
                parts = line.split('\t')
                if len(parts) < 3:
                    continue

                # Extract the relevant fields
                symbol = parts[0]  # Function name
                file_path = parts[1]  # File path
                signature = parts[3][10:]  # Function signature
                parsed_data.append({
                    "symbol": symbol,
                    "file": file_path,
                    "signature": signature,
                    "count": 0,
                })
            except Exception as e:
                print(f"Error parsing line: {line}\n{e}")
    return parsed_data

def get_ctags_output(file_path):
    ctags_cmd=['ctags', '-x','--c-kinds=f', '--c++-kinds=f','--fields=S', file_path]
    t,output=execute_command(ctags_cmd,timeout=1200)
    if t:
        return output
    else:
        print("Error running ctags:", output)
        return None

def extract_entry_funs(file_path):
    ctags_output = get_ctags_output(file_path)
    entry_functions = []
    if ctags_output:
        for line in ctags_output.strip().split("\n"):
            entry_functions.append(line.split()[0])
    return entry_functions

# Generate cscope_db for querying function call relationships
def generate_cscope_db(input_dir: str, output_file: str, extensions=(".c", ".h",".cpp",".hpp",".cc",".hh",".cxx",".hxx",".c++",".h++")):
    input_dir = Path(input_dir).resolve()
    output_file = Path(output_file)
    cscope_files = output_file.parent / "cscope.files"

    lower_extensions = {ext.lower() for ext in extensions}
    source_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in lower_extensions:
                full_path = Path(root) / file
                source_files.append(str(full_path))

    if not source_files:
        print(f"No source files found in {input_dir} with extensions {extensions}")
        return False,cscope_files
    with open(cscope_files, "w") as f:
        f.write("\n".join(source_files))

    cmd = [
        "cscope",
        "-b",  
        "-i", str(cscope_files),  
        "-f", str(output_file),  
        "-q"  
    ]
    t,output=execute_command(cmd,timeout=1800)
    if not t:
        print("Error running cscope:", output)
        return False,cscope_files
    else:
        print(f"Cscope database generated at: {output_file}")
        return True,cscope_files

def modify_main_function(file_path):
    try:
        with open(file_path, 'r',errors='ignore') as file:
            content = file.read()
        main_pattern = r'\bint\s+main\s*\('
        if re.search(main_pattern, content):
            print(f"'main' function found in {file_path}. Modifying...")
            modified_content = re.sub(main_pattern, 'int main_(', content)
            with open(file_path, 'w',errors='ignore') as file:
                file.write(modified_content)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Convert compilation commands to clang syntax
def sanitize_clang_command(command: str) -> str:
    SUPPORT_RULES = {
        'remove': {
            '-ffat-lto-objects',
            '-fconserve-stack',
            '-fno-var-tracking',
            '-fno-var-tracking-assignments',
            '-fno-var-tracking-uninit',
            '-fuse-linker-plugin',          
            '-mindirect-branch=thunk-extern',  
            '-mpreferred-stack-boundary=3',   
            '-fno-stack-protector',         
            '-fdirectives-only',            
            '-fno-ident',                   
            '-fno-asynchronous-unwind-tables',
            '-fno-reorder-blocks-and-partition'  
            
        },
        'replace': {
            '-flto=auto': '-flto',          
            '-flto=jobserver': '-flto',
            '-fno-plt': '-fno-pic',         
            '-march=ivybridge': '-march=x86-64',  
            '-mtune=generic': '-mcpu=generic',
            '-Wformat-overflow=2': '-Wformat',  
            '-Wstringop-overflow=4': '-Wstring-plus-int',
            '-fplugin=annobin.so': '',      
            '-fipa-pta': '-fno-ipa-pta',    
            '-fstack-clash-protection': '-fstack-protector',
            '-fsched-pressure': '',          
            '-fanalyzer': ''
        },
        'prefix_replace': {
            '-march=': '-march=x86-64',     
            '-mtune=': '-mcpu=generic',
            '-Wa,': '',                     
            '-Wl,': ''                      
        }
    }
    args = command.split()
    new_args = []

    for arg in args:
        if arg in SUPPORT_RULES['replace']:
            replacement = SUPPORT_RULES['replace'][arg]
            if replacement:
                new_args.append(replacement)
            continue
        replaced = False
        for prefix, replacement in SUPPORT_RULES['prefix_replace'].items():
            if arg.startswith(prefix):
                if replacement:
                    new_args.append(replacement)
                replaced = True
                break
        if replaced:
            continue
        if arg in SUPPORT_RULES['remove']:
            continue
        new_args.append(arg)
    escaped_args = []
    for arg in new_args:
        if ' ' in arg and not (arg.startswith(('"', "'"))):
            escaped_args.append(f'"{arg}"')
        else:
            escaped_args.append(arg)

    return ' '.join(escaped_args)

def modify_compile_command(command, output_file):
    command=sanitize_clang_command(command)
    args = command.split()
    original_compiler = args[0]
    if "++" in original_compiler or original_compiler.endswith("cpp"):
        compiler = "clang++-10"
    else:
        compiler = "clang-10"
    args[0] = compiler
    additional_flags = ["-c", "-g", "-emit-llvm","-O0", "-fno-inline", "-Xclang", "-disable-O0-optnone", "-fno-discard-value-names", "-fno-eliminate-unused-debug-types"]
    for flag in additional_flags:
        if flag not in args:
            args.insert(1, flag) 
    if "-o" in args:
        index = args.index("-o")
        if index + 1 < len(args):
            args[index + 1] = output_file
    escaped_command = ' '.join(arg for arg in args)
    return escaped_command

def compile_to_bc(compile_cmd,file_path,bc_folder):
    bc_file=bc_folder+"/"+os.path.splitext(os.path.basename(file_path))[0]+".bc"
    bc_compile_command=modify_compile_command(compile_cmd["command"],bc_file)
    execute_command(bc_compile_command)
    clean_exception_cmd="opt-10 -lowerinvoke "+bc_file+" -o "+bc_file
    execute_command(clean_exception_cmd)
    ll_file=bc_folder+"/"+os.path.splitext(os.path.basename(file_path))[0]+".ll"
    generate_ll_cmd="llvm-dis-10 "+bc_file+" -o "+ll_file
    execute_command(generate_ll_cmd)
    return bc_file,ll_file

def llvm_link_bc(bc_file_chain,result_main_bc_file,bc_file,slice_fun_bc_file):
    if len(bc_file_chain)==1:
        link_bc_command="llvm-link-10 " + " ".join(bc_file_chain) + " -o "+result_main_bc_file
    else:
        link_bc_command="llvm-link-10 --override " + " ".join(bc_file_chain) + " -o "+result_main_bc_file
    execute_command(link_bc_command)
    if not os.path.exists(result_main_bc_file) or os.path.getsize(result_main_bc_file) == 0:
        bc_file_chain=[bc_file,slice_fun_bc_file]
        link_bc_command="llvm-link-10 --override " + " ".join(bc_file_chain) + " -o "+result_main_bc_file
        execute_command(link_bc_command)
        if not os.path.exists(result_main_bc_file) or os.path.getsize(result_main_bc_file) == 0:
            bc_file_chain=[bc_file]
            link_bc_command="llvm-link-10 " + " ".join(bc_file_chain) + " -o "+result_main_bc_file
            execute_command(link_bc_command)

    return result_main_bc_file


def insert_headers(file_path, headers):
    try:
        with open(file_path, 'r',errors='ignore') as file:
            content = file.read()
        header_lines = ''.join([f'{header}\n' for header in headers])
        new_content = header_lines + '\n' + content
        with open(file_path, 'w',errors='ignore') as file:
            file.write(new_content)
    except Exception as e:
        print(f"Error inserting headers into {file_path}: {e}")

def generate_command(arguments, directory):
    updated_args = []
    for arg in arguments:
        if arg.startswith("-I"):
            path = arg[2:] 
            if not os.path.isabs(path):
                path = os.path.join(directory, path)
            updated_args.append(f"-I{shlex.quote(os.path.abspath(path))}")
        elif not arg.startswith("-") and os.path.exists(os.path.join(directory, arg)):
            updated_args.append(shlex.quote(os.path.abspath(os.path.join(directory, arg))))
        else:
            updated_args.append(shlex.quote(arg))
    return ' '.join(updated_args)

def add_command_field(data):
    for item in data:
        if "arguments" in item:
            full_command = generate_command(item["arguments"], item.get("directory", ""))
            item["file_path"] = os.path.abspath(os.path.join(item.get("directory", ""), item.get("file", "")))
            item["command"] = full_command
    return data

def del_duplicate(data):
    seen = set()      
    result = []       

    for item in data:
        path = item["file_path"]
        if path not in seen:
            seen.add(path)
            result.append(item)
    return result

def process_compile_commands(input_file, output_file):
    data = read_json_file(input_file)
    updated_data = add_command_field(data)
    updated_data = del_duplicate(updated_data)
    write_json_file(output_file, updated_data)
    print("compile_cmds file generated successfully.")

