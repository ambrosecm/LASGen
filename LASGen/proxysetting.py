import os
def initproxy():

    os.environ["AFL_USE_ASAN"] = "1"
    os.environ["AFL_USE_UBSAN"] = "1"
    return

initproxy()

# afl-fuzz time limit
hour=4
# Set the maximum thread pool size (number of concurrently executing LLM instances)
llm_max_threads = 10
# Set the maximum thread pool size (number of concurrently executing AFL instances)
afl_max_threads = 180

# LLM settings
# Set the base URL for the LLM API
base_url=""
# Set the API key for the LLM
api_key=""
# Set the model to be used for LLM
use_model="deepseek-chat"
# Set the model to be used for embeddings API
base_url_embeddings=""
# Set the API key for the embeddings API
api_key_embeddings=""

# set target library settings
# libjasper example
# Library version id
lib_id="2.0.14"
# Library path
lib_directory="../TestLib/jasper"
# bear generated compile command file path
compile_cmds_file = '../TestLib/jasper_build/compile_commands.json'
# The static or dynamic library path
LD_lib_path="../TestLib/jasper_build/src/libjasper/libjasper.so"
# List of target functions to be fuzzed. If None, fuzzing will be performed for all functions
vul_fun_list=[""]