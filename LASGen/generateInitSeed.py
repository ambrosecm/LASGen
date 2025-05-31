import subprocess
import os
import llm_generate
from util import *

def create_folder(folder_path):
    try:
        # os.makedirs can recursively create directories, and will also create parent directories if they do not exist.
        os.makedirs(folder_path, exist_ok=True)
        print(f"The folder '{folder_path}' has been created or already exists.")
        return True
    except Exception as e:
        print(f"An error occurred while creating the folder '{folder_path}': {e}")
        return False


def savecode(code, path):
    with open(path, 'w') as f:
        f.write(str(code) if code is not None else "")

def execute_pycode(pycode_path, timeout=300):
    if not os.path.isfile(pycode_path):
        return False, f"Error: File {pycode_path} not found."
    cmd=["python3", pycode_path]
    t,output=execute_command(cmd,timeout=timeout)
    return t,output

# Check whether the seed file has been generated and whether there is a program in the folder that can run the seed.
def check_init_seed(init_seed_file_path,harness_program_file,init_seed_dir):
    print('=========Check seed file=========')
    if not os.path.exists(init_seed_file_path):
        return False
    parent_dir = os.path.dirname(init_seed_dir)  
    outputdir = os.path.join(parent_dir, "output")  
    # Create a temporary folder for storing output
    tmp_dir=os.path.join(outputdir,"tmp")
    create_folder(tmp_dir)
    # Iterate through the init_seed_dir folder
    for seed_file in os.listdir(init_seed_dir):
        seed_file_path = os.path.join(init_seed_dir, seed_file)
        # Check if it is a file (excluding subdirectories)
        if os.path.isfile(seed_file_path):
            cmd=[harness_program_file, seed_file_path]
            t,r=execute_command(cmd,timeout=5,tmp_dir=tmp_dir,flag=1)
            if t:
                print("Execution successful, executable seed file exists.")
                return True  # As long as one file executes successfully, immediately return True.
    print("Execution failed, no executable seed file exists.")
    return False  # All files failed to execute, returning False

# Generate seed file
def generate_init_seed_by_LLM(sliced_code_forward_file,harness_code_file,slice_fun,slice_fun_code,init_seed_dir,harness_program_file,rag_chain):
    print('=========Generate seed file=========')
    if not os.path.exists(sliced_code_forward_file):
        sliced_forward_code=""
    else:
        with open(sliced_code_forward_file, 'r') as file:
            sliced_forward_code = file.read()
    with open(harness_code_file, 'r') as file:
        harness_code = file.read()
    # Get harness input type
    harness_input_type=llm_generate.get_harness_input_type(harness_code).input_type
    print(harness_input_type)
    # Initial seed file path
    init_seed_file_name="0"
    init_seed_file_path=init_seed_dir+"/input/"+init_seed_file_name
    init_seed_generate_code_file_path=init_seed_dir+"/"+init_seed_file_name+".py"

    # Create an initial seed storage directory
    os.makedirs(os.path.dirname(init_seed_file_path), exist_ok=True)

    init_seed_generate_file_code=""
    # Python code for generating the initial seed file
    if harness_input_type=="normal":
        init_seed_generate_file_code=llm_generate.generate_init_seed(sliced_forward_code,harness_code,slice_fun,slice_fun_code,rag_chain,init_seed_file_path)
    elif harness_input_type=="file":
        init_seed_generate_file_code=llm_generate.generate_init_seed_generate_file(sliced_forward_code,harness_code,slice_fun,slice_fun_code,rag_chain,init_seed_file_path)
    # Save the code that generates the initial seed file.
    savecode(init_seed_generate_file_code,init_seed_generate_code_file_path)
    # Execute seed generation file to generate seed
    execute_pycode(init_seed_generate_code_file_path)

    f=1
    while not check_init_seed(init_seed_file_path,harness_program_file,init_seed_dir+"/input"):
        init_seed_file_path=init_seed_dir+"/input/"+str(f)
        init_seed_generate_code_file_path=init_seed_dir+"/"+str(f)+".py"
        if f<5:
            if harness_input_type=="normal":
                init_seed_generate_file_code=llm_generate.generate_init_seed(sliced_forward_code,harness_code,slice_fun,slice_fun_code,rag_chain,init_seed_file_path)
            elif harness_input_type=="file":
                init_seed_generate_file_code=llm_generate.generate_init_seed_generate_file(sliced_forward_code,harness_code,slice_fun,slice_fun_code,rag_chain,init_seed_file_path)
            # Save the code that generates the initial seed file.
            savecode(init_seed_generate_file_code,init_seed_generate_code_file_path)
            execute_pycode(init_seed_generate_code_file_path)
        else:
            break
        f+=1

    return init_seed_dir+"/input"
