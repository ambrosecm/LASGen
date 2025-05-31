from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from langchain.chains import create_retrieval_chain
from langchain_core.messages import AIMessage
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import EnsembleRetriever
from langchain_community.chat_message_histories import SQLChatMessageHistory
import re
import proxysetting
import time
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3")
max_tokens=30000
base_url=proxysetting.base_url
api_key=proxysetting.api_key
base_url_embeddings=proxysetting.base_url_embeddings
api_key_embeddings=proxysetting.api_key_embeddings
use_model=proxysetting.use_model

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

# Generate a database for the searcher
def generateVecDB(kb_dir,flag):
    if flag is None:
        return None
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(kb_dir, glob="./*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs, silent_errors=True)
    docs = loader.load()
    readme_content = docs[0].page_content
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    md_splitter_docs = markdown_splitter.split_text(readme_content)
    embeddings_model = OpenAIEmbeddings(base_url=base_url_embeddings,api_key=api_key_embeddings)
    max_retries=5
    retry_delay=5
    retries = 0
    while retries < max_retries:
        try:
            vectorstoredb = Chroma.from_documents(
                documents=md_splitter_docs, 
                embedding=embeddings_model
                )
            return vectorstoredb
        except TimeoutError:
            retries += 1
            if retries < max_retries:
                print(f"Timeout occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return None
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"Exception occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return None

# Create a normal Q&A chain
def generate_normal_llm_chain(temperature):
    llm = ChatOpenAI(model=use_model,base_url=base_url,api_key=api_key,temperature=temperature)
    system_prompt = (
        "You are a programmer who is very familiar with programming. "
        "Please answer the question. If you don't know the answer, say that you "
        "don't know. Keep the answer concise."
        "\n\n"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    rag_chain = prompt | llm
    return rag_chain

def get_normal_llm_chain_dict(temperature):
    rag_chain = generate_normal_llm_chain(temperature)
    rag_chain = {"rag_chain": rag_chain,"flag":None}
    return rag_chain

# Create a rag chain with no history
def generate_RAG_chain_without_history(vectorstoredb,temperature):
    llm = ChatOpenAI(model=use_model,base_url=base_url,api_key=api_key,temperature=temperature)
    if vectorstoredb is None:
        return get_normal_llm_chain_dict(temperature)
    similar_retriever = vectorstoredb.as_retriever(search_type="similarity")
    mmr_retriever = vectorstoredb.as_retriever(search_type="mmr")
    ensemble_retriever = EnsembleRetriever(
        retrievers=[similar_retriever, mmr_retriever], weights=[0.5, 0.5]
    )
    compression_retriever=ensemble_retriever
    system_prompt = (
        "You are a programmer who is very familiar with programming. "
        "Use the following pieces of retrieved context code to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Keep the answer concise."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(compression_retriever, question_answer_chain)
    rag_chain = {"rag_chain": rag_chain,"flag":1}
    return rag_chain


def RAG_chat(input_prompt, conversational_rag_chain, max_retries=5, retry_delay=3):
    encoded = tokenizer.encode(input_prompt, add_special_tokens=False)
    truncated_tokens = encoded[:max_tokens]
    input_prompt=tokenizer.decode(truncated_tokens, skip_special_tokens=True)
    retries = 0
    while retries < max_retries:
        try:
            response = conversational_rag_chain.invoke(
                {
                    "input": input_prompt,
                },
            )
            return response
        except TimeoutError:
            retries += 1
            if retries < max_retries:
                print(f"Timeout occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return ""
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"Exception occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return ""

    return ""


def harness_response_parse(ai_message: AIMessage) -> str:
    markdown_text=ai_message['answer']
    extracted_code = None
    start_index = markdown_text.find('```')
    end_index = markdown_text.find('```', start_index + 3)
    if (start_index==-1 or end_index==-1):
        return None
    if markdown_text.find('#include',start_index,end_index) ==-1:
        return None
    if re.search(markdown_text[start_index:start_index + 6], "```cpp", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 6:end_index].strip()
    elif re.search(markdown_text[start_index:start_index + 4], "```c", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 4:end_index].strip()
    return extracted_code

def harness_response_parse2(ai_message: AIMessage) -> str:
    markdown_text=ai_message.content
    extracted_code = None
    start_index = markdown_text.find('```')
    end_index = markdown_text.find('```', start_index + 3)
    if (start_index==-1 or end_index==-1):
        return None
    if markdown_text.find('#include',start_index,end_index) ==-1:
        return None
    if re.search(markdown_text[start_index:start_index + 6], "```cpp", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 6:end_index].strip()
    elif re.search(markdown_text[start_index:start_index + 4], "```c", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 4:end_index].strip()
    return extracted_code


def generate_harness(sliced_code,slice_fun,slice_fun_code,code_type,ragchain):
    rag_chain=ragchain["rag_chain"]
    flag=ragchain["flag"]
    input_prompt = (
        "Now you are a fuzz testing expert, and you are very good at generating function driver code for AFL (American Fuzzy Lop). \n"
        f"The following <slice code> is the slice code for the calling process of the {slice_fun} function. Your task is to fix the following slice code into a complete and executable code to call the {slice_fun} function. Finally, you will get a complete driver code for fuzz testing of the {slice_fun} function. Please refer to the following process for thinking and generation: \n"
        f"1. Learn the variables required to call the function in the <slice code>, and set the necessary pre-variables before calling the {slice_fun} function. \n"
        f"2. You need to add a `main` function in the generated code, which is responsible for calling the {slice_fun} function and passing the input to the parameters of the {slice_fun} function. Learn the calling process in the <slice code>, and fix the complete {slice_fun} function calling code through the <slice code>. \n"
        f"3. If the parameter contains flags, please first analyze the parameter type and flag settings in the definition code of the {slice_fun} function, and then try multiple combinations of flags when generating code to help the program cover more function code paths when running.\n"
        f"4. The input data will be passed in the form of a file, which contains the input of important parameters of the {slice_fun} function. The program has only one input file, and the running format of the program and input file is [$ ./program ./inputfile]. You need to add an input file processing module in the `main` function. The function of this module is to read the content of the corresponding file through the file name passed by the `main` function, parse the content into the format required by the {slice_fun} function, and then pass it to the function. Please note that **the parameters in the {slice_fun} function should be determined by passing in the file instead of specifying it directly in the code**.\n"
        f"5.Please note that it is not allowed to modify or delete the header files related to the target library provided in the slice code. You can add, modify, and delete the standard library header files. Please refer to the standard library in the Linux system for modification. Please adjust the order of the header files. The standard library header files should be placed first, and the header files related to the target library should be placed at the end. If you encounter header files .h and .c with the same name, please keep the .c header file, because some functions called may not be declared in the .h header file or the .h file does not exist. **\n"
        f"6.**You do not need to provide the implementation of the {slice_fun} function or other APIs in the calling code. They are already defined in the header file. Do not define them repeatedly**. The key is how to call the function and pass the input. \n"
        f"7.**Do not use non-existent functions in the code**. All functions should exist in reality. You can learn these functions from the knowledge base retrieved from the slice code. \n"
        f"8.**Reduce input correctness checks**, because the purpose of this code is to test whether there are vulnerabilities in the function in the library, so there is no need to check the input of the function. \n"
        f"9.{slice_fun} needs to release resources after the function call.\n\n"
        f"Please use {code_type} code to implement it.\n"
        "The final format reference is as follows. \n"
        "Code: \n"
        "#include <> // library header file \n"
        "int main() //pass input files\n"
        "{ \n"
        "//the library API code \n"
        "} \n"
        f"<{slice_fun} function definition code>：\n"
        f"[{slice_fun_code}]\n"
        "<Slice code>：\n"
        f"[{sliced_code}\n]"
        "Example：{C language code example：\n"
        "[example 1：\n"
        "<Slice code>：\n"
        "#include <stdio.h> \n"
        "#include <stdlib.h> \n"
        '#include "computer.h" \n'
        '#include "example.c" \n'
        "16: int test(int x, int y) \n"
        "17: { \n"
        "20:     compute(x, y); \n"
        "23: } \n"
        "<compute function code>：\n"
        "void compute(int a, int b) \n"
        "{ \n"
            "int c = a + b; \n"
            "int d = c * 2; \n"
            "int e = d - a; \n"
            "std::cout << e << std::endl; \n"
            "show(e, a); \n"
        "} \n"
        "<Output code>：\n"
        "#include <stdio.h> \n"
        "#include <stdlib.h> \n"
        '#include "computer.h" \n'
        '#include "example.c" \n'
        "int main(int argc, char *argv[]) \n"
        "{ \n"
            "if (argc != 2) \n"
            "{ \n"
                'fprintf(stderr, "Usage: %s <input_file>\n", argv[0]); \n'
                "return 1; \n"
            "} \n"
            "// Opening a file \n"
            'FILE *inputFile = fopen(argv[1], "r"); \n'
            "if (!inputFile) \n"
            "{ \n"
                'fprintf(stderr, "Error opening file: %s\n", argv[1]); \n'
                "return 1; \n"
            "} \n"
            "int x, y; \n"
            "// Read two integers from a file \n"
            'if (fscanf(inputFile, "%d %d", &x, &y) != 2) \n'
            "{ \n"
                'fprintf(stderr, "Error reading integers from file.\n"); \n'
                "fclose(inputFile); \n"
                "return 1; \n"
            "} \n"
            "// Close File \n"
            "fclose(inputFile); \n"
            "// Calling the calculation function \n"
            "compute(x, y); \n"
            "return 0; \n"
        "} \n"
        "example 2：\n"
        "<slice code>：\n"
        '#include "stdlib.h"\n'
        '#include "stdio.h"\n'
        '#include "string.h"\n'
        '#include "jfif.h"\n'
        '#include "bmp.h"\n'
        '#include "ffjpeg.c"\n'
        '8: int main_(int argc, char *argv[])\n'
        '9: {\n'
        '10:     void *jfif = NULL;\n'
        "11:     BMP   bmp  = {0};\n"
        '13:     if (argc < 3) {\n'
        '22:     if (strcmp(argv[1], "-d") == 0) {\n'
        '28:     } else if (strcmp(argv[1], "-e") == 0) {\n'
        '29:         if (bmp_load(&bmp, argv[2]) == -1) {\n'
        '37:     }\n'
        '40: }\n'
        "<bmp_load function code>：\n"
        '30: int bmp_load(BMP *pb, char *file)\n'
        '31: {\n'
        '32:     BMPFILEHEADER header = {0};\n'
        '33:     FILE         *fp     = NULL;\n'
        '34:     BYTE         *pdata  = NULL;\n'
        '35:     int           i;\n'
        '37:     fp = fopen(file, "rb");\n'
        '38:     if (!fp) return -1;\n'
        '40:     fread(&header, sizeof(header), 1, fp);\n'
        '41:     pb->width  = (int)header.biWidth  > 0 ? (int)header.biWidth  : 0;\n'
        '42:     pb->height = (int)header.biHeight > 0 ? (int)header.biHeight : 0;\n'
        '43:     pb->stride = ALIGN(pb->width * 3, 4);\n'
        '44:     if ((long long)pb->stride * pb->height >= 0x80000000) {\n'
        "45:         printf(\"bmp's width * height is out of range !\");\n"
        '46:         goto done;\n'
        '47:     }\n'
        '48:     pb->pdata  = malloc((size_t)pb->stride * pb->height);\n'
        '49:     if (pb->pdata) {\n'
        '50:         pdata  = (BYTE*)pb->pdata + pb->stride * pb->height;\n'
        '51:         for (i=0; i<pb->height; i++) {\n'
        '52:             pdata -= pb->stride;\n'
        '53:             fread(pdata, pb->stride, 1, fp);\n'
        '54:         }\n'
        '55:     }\n'
        '57: done:\n'
        '58:     if (fp) fclose(fp);\n'
        '59:     return pb->pdata ? 0 : -1;\n'
        '60: }\n'
        "<output code>：\n"
        '#include <stdlib.h>\n'
        '#include <stdio.h>\n'
        '#include <string.h>\n'
        '#include "jfif.h"\n'
        '#include "bmp.h"\n'
        '#include "ffjpeg.c"\n'
        'int main(int argc, char *argv[])\n'
        '{\n'
            'BMP bmp = {0};\n'
            'if (argc < 2) {\n'
                'fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);\n'
                'return 1;\n'
            '}\n'
            'if (bmp_load(&bmp, argv[1]) == -1) {\n'
                'fprintf(stderr, "Failed to load BMP file: %s", argv[1]);\n'
                'return 1;\n'
            '}\n'
            'if (bmp.pdata) {\n'
                'free(bmp.pdata);\n'
            '}\n'
            'return 0;\n'
        '}\n'
        "] \n"
        "C++ code example：\n"
        "[<slice code>："
        "#include <iostream> \n"
        '#include "computer.cpp" \n'
        '#include "example.cpp" \n'
        "16: int test(int x, int y) \n"
        "17: { \n"
        "20:     compute(x, y); \n"
        "23: } \n"
        "<compute function code>："
        "void compute(int a, int b) \n"
        "{ \n"
            "int c = a + b; \n"
            "int d = c * 2; \n"
            "int e = d - a; \n"
            "std::cout << e << std::endl; \n"
            "show(e, a); \n"
        "} \n"
        "<output code>："
        "#include <iostream> \n"
        "#include <fstream> // For file operations \n"
        "#include <cstdlib> \n"
        '#include "computer.cpp" \n'
        '#include "example.cpp" \n'
        "int main(int argc, char *argv[]) \n"
        "{ \n"
            "if (argc != 2) \n"
            "{ \n"
                'std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl; \n'
                "return 1; \n"
            "} \n"
            "// open file \n"
            "std::ifstream inputFile(argv[1]); \n"
            "if (!inputFile) \n"
            "{ \n"
                'std::cerr << "Error opening file: " << argv[1] << std::endl; \n'
                "return 1; \n"
            "} \n"
            "int x, y; \n"
            "inputFile >> x >> y; \n"
            "if (inputFile.fail()) \n"
            "{ \n"
                'std::cerr << "Error reading integers from file." << std::endl; \n'
                "return 1; \n"
            "} \n"
            "compute(x, y); \n"
            "return 0; \n"
        "} \n"
        "] \n"
        "}\n"
    )
    if flag is None:
        chain=rag_chain | harness_response_parse2
    else:
        chain=rag_chain | harness_response_parse

    response=RAG_chat(input_prompt,chain)
    return response,input_prompt

def generate_harness_without_slicecode(slice_fun,slice_fun_code,headers,code_type,ragchain):
    rag_chain=ragchain["rag_chain"]
    flag=ragchain["flag"]
    headers=",".join(headers)
    input_prompt = (
        "Now you are a fuzz testing expert, and you are very good at generating function driver code for AFL (American Fuzzy Lop). \n"
        f"The code of the {slice_fun} function is provided below. Your task is to learn the calling method of the function and generate the complete calling code of the function in order to call the {slice_fun} function. Finally, you will get a complete driver code for fuzz testing of the {slice_fun} function. Please refer to the following process for thinking and generation: \n"
        f"1. Learn the code of the {slice_fun} function, infer the variables required for calling {slice_fun}, and set the necessary pre-variables before calling the {slice_fun} function. \n"
        f"2. Please note that **please add the necessary header files (the file needs to be ensured to exist), and the header files included in the header file list [{headers}] must be added, otherwise it will cause compilation errors**. You can add, modify, and delete standard header files. Refer to the standard library in the Linux system for modification. \n"
        f"3.Please note that **it is not allowed to modify or delete the header files related to the provided target library. You can add, modify, and delete the standard library header files. Please refer to the standard library in the Linux system for modification. Please adjust the order of the header files. The standard library header files should be placed first, and the header files related to the target library should be placed at the end. If you encounter header files .h and .c with the same name, please keep the .c header file, because some functions called may not be declared in the .h header file or the .h file does not exist.**\n"
        f"4.You need to add a `main` function in the generated code, which is responsible for calling the {slice_fun} function and passing the input to the parameters of the {slice_fun} function.\n"
        f"5.If the parameters contain flags, please first analyze the parameter type and flag settings in the definition code of the {slice_fun} function, and then try multiple combinations of flags when generating code to help the program run to cover more function code paths.\n"
        f"6.The input data will be passed in as a file, which contains {slice_fun} The input of important parameters of the function. The program has only one input file, and the running format of the program and input file is [$ ./program ./inputfile]. You need to add an input file processing module in the `main` function. The function of this module is to read the content of the corresponding file through the file name passed by the `main` function, and parse the content into the format required by the {slice_fun} function, and then pass it to the function. Please note that **the parameters in the {slice_fun} function should be determined by passing in the file instead of specifying them directly in the code**. \n"
        f"7.**You do not need to provide the implementation of the {slice_fun} function or call other APIs in the code. They have been defined in the header file. Do not define them repeatedly**. The key point is how to call the function and pass the input. \n"
        f"8.**Do not use non-existent functions in the code**. All functions should really exist. You can learn these functions from the slice code and the retrieved knowledge base. \n"
        f"9.**Reduce input correctness check**, because the purpose of this code is to test whether there are vulnerabilities in the function in the library, so there is no need to check the input of the function.\n"
        f"10.{slice_fun} needs to release resources after the function call.\n\n"
        f"Please use {code_type} code to implement it. \n"
        "The final format reference is as follows. \n"
        "Code: \n"
        "#include <> // library header file \n"
        "int main() //pass input files\n"
        "{ \n"
        "//the library API code \n"
        "} \n"
        f"<{slice_fun} function definition code>：\n"
        f"[{slice_fun_code}]\n"
        "example：{C language code example：\n"
        "[<compute function code>："
        "void compute(int a, int b) \n"
        "{ \n"
            "int c = a + b; \n"
            "int d = c * 2; \n"
            "int e = d - a; \n"
            "std::cout << e << std::endl; \n"
            "show(e, a); \n"
        "} \n"
        "<output code>："
        "#include <stdio.h> \n"
        "#include <stdlib.h> \n"
        '#include "computer.h" \n'
        '#include "example.c" \n'
        "int main(int argc, char *argv[]) \n"
        "{ \n"
            "if (argc != 2) \n"
            "{ \n"
                'fprintf(stderr, "Usage: %s <input_file>\n", argv[0]); \n'
                "return 1; \n"
            "} \n"
            'FILE *inputFile = fopen(argv[1], "r"); \n'
            "if (!inputFile) \n"
            "{ \n"
                'fprintf(stderr, "Error opening file: %s\n", argv[1]); \n'
                "return 1; \n"
            "} \n"
            "int x, y; \n"
            'if (fscanf(inputFile, "%d %d", &x, &y) != 2) \n'
            "{ \n"
                'fprintf(stderr, "Error reading integers from file.\n"); \n'
                "fclose(inputFile); \n"
                "return 1; \n"
            "} \n"
            "fclose(inputFile); \n"
            "compute(x, y); \n"
            "return 0; \n"
        "} \n"
        "] \n"
        "C++ code example：\n"
        "[<compute function code>："
        "void compute(int a, int b) \n"
        "{ \n"
            "int c = a + b; \n"
            "int d = c * 2; \n"
            "int e = d - a; \n"
            "std::cout << e << std::endl; \n"
            "show(e, a); \n"
        "} \n"
        "<output code>："
        "#include <iostream> \n"
        "#include <fstream>  \n"
        "#include <cstdlib>  \n"
        '#include "computer.h" \n'
        '#include "example.cpp" \n'
        "int main(int argc, char *argv[]) \n"
        "{ \n"
            "if (argc != 2) \n"
            "{ \n"
                'std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl; \n'
                "return 1; \n"
            "} \n"
            "std::ifstream inputFile(argv[1]); \n"
            "if (!inputFile) \n"
            "{ \n"
                'std::cerr << "Error opening file: " << argv[1] << std::endl; \n'
                "return 1; \n"
            "} \n"
            "int x, y; \n"
            "inputFile >> x >> y; \n"
            "if (inputFile.fail()) \n"
            "{ \n"
                'std::cerr << "Error reading integers from file." << std::endl; \n'
                "return 1; \n"
            "} \n"
            "compute(x, y); \n"
            "return 0; \n"
        "} \n"
        "] \n"
        "}\n"
    )
    if flag is None:
        chain=rag_chain | harness_response_parse2
    else:
        chain=rag_chain | harness_response_parse
    response=RAG_chat(input_prompt,chain)
    return response,input_prompt

def re_generate_harness_with_error(ragchain,error_msg,init_harness,code_generate_prompt):
    rag_chain=ragchain["rag_chain"]
    flag=ragchain["flag"]
    input_prompt = (
        "You are now a programmer who is very good at modifying code compilation errors. \n"
        "When compiling the <Generated code> code, the following error message <error message> appears. Please refer to the error message <error message> and the input prompt <code_generate_prompt> of the generated code to modify the <Generated code (to be modified)> code to help it compile successfully. (Please note that you only need to modify the error prompt and ignore the warning prompt): \n"
        "When you modify the code, you can refer to the following prompts: \n"
        "1. If an error message is reported for a function undefined reference, try to change the .h file of the related library called in the header file to .c or delete the problematic .c header file. \n"
        "2. If an error message appears for a system library header file, please refer to the standard library in the Linux system for modification. If the header file does not belong to the Linux system, please change it to the correct header file. Please adjust the order of the header files. The standard library header file should be placed first, and the header files related to the target library should be placed at the end. \n"
        "3. If an error message is included multiple times, delete the duplicate header files introduced in the code. \n"
        "4. If the error multiple definition is reported, check whether the .h and .c header files with the same name related to the library are included at the same time. In this case, please keep only the .h header file or only the .c header file.\n"
        "4. If there is a problem with the header file import, the error typedef redefinition with different types is reported. Delete the problematic .c header file.\n"
        "5. If the error file not found is reported for a certain header file, please delete the corresponding header file or change the header file from .h to .c.\n"
        "6. When a syntax error occurs, please refer to the input prompt to modify the relevant error.\n"
        "7. When a variable is undefined, please check whether the relevant header file is imported.\n"
        "8. When a function is undefined, please check whether the relevant header file is imported.\n"
        "9. When the function parameters do not match, please check the correct parameters of the function.\n"
        "10. You do not need to provide the implementation of the API in the calling code. They are already defined in the header file. Do not define them again.\n"
        
        
        f"<error massage>: [{error_msg}] \n"
        f"<Generated code (to be modified)>: [{init_harness}] \n"
        f"<code_generate_prompt>: [{code_generate_prompt}] \n"
    )
    if flag is None:
        chain=rag_chain | harness_response_parse2
    else:
        chain=rag_chain | harness_response_parse
    response=RAG_chat(input_prompt,chain)
    return response

# Defining input types
class harness_input_type(BaseModel):
    input_type: str = Field(description="The input data type of the code. Optional: 'normal' or 'file'.")

# Parse the input data type in the code, whether to use the code to generate the input file, if yes, return file, otherwise return normal
def get_harness_input_type(harness_code):
    parser = PydanticOutputParser(pydantic_object=harness_input_type)
    input_prompt = (
        f"Please analyze the input data type of the following code. If the input is a general data type, return 'normal'; if it is other complex data types, return 'file'\n"
        f"{harness_code} \n"
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
        ),
        ("human", "{query}"),
    ]
    ).partial(format_instructions=parser.get_format_instructions())
    llm=ChatOpenAI(model=use_model,api_key=api_key,base_url=base_url,temperature=0.2)
    chain = prompt | llm | parser
    max_retries=5
    retry_delay=3
    retries = 0
    while retries < max_retries:
        try:
            input_type=chain.invoke({"query": input_prompt})
            return input_type
        except TimeoutError:
            retries += 1
            if retries < max_retries:
                print(f"Timeout occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return "normal"
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"Exception occurred. Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return "normal"

    return "normal"


# Parse the code to generate the input file
def init_seed_generate_codefile_parse(ai_message: AIMessage) -> str:
    markdown_text=ai_message['answer']
    extracted_code = None
    start_index = markdown_text.find('```')
    end_index = markdown_text.find('```', start_index + 3)
    if (start_index==-1 or end_index==-1):
        return None
    if re.search(markdown_text[start_index:start_index + 9], "```python", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 9:end_index].strip()
    return extracted_code

# Parse the code to generate the input file
def init_seed_generate_codefile_parse2(ai_message: AIMessage) -> str:
    markdown_text=ai_message.content
    extracted_code = None
    start_index = markdown_text.find('```')
    end_index = markdown_text.find('```', start_index + 3)
    if (start_index==-1 or end_index==-1):
        return None
    if re.search(markdown_text[start_index:start_index + 9], "```python", re.IGNORECASE):
        extracted_code = markdown_text[start_index + 9:end_index].strip()
    return extracted_code

# Code to generate harness input file: normal
def generate_init_seed(sliced_forward_code,harness_code,slice_fun,slice_fun_code,ragchain,init_seed_file_path):

    encoded = tokenizer.encode(sliced_forward_code, add_special_tokens=False)
    truncated_tokens = encoded[:8000]
    sliced_forward_code=tokenizer.decode(truncated_tokens, skip_special_tokens=True)

    rag_chain=ragchain["rag_chain"]
    flag=ragchain["flag"]
    input_prompt = (
        f"Now you need to generate a python code. The purpose of the code is to generate the input of [harness_code] and save it in a file. The generated file path is [{init_seed_file_path}]. The generated input file is used for subsequent fuzz testing of [harness_code]. It is necessary to ensure that the harness program can run correctly when using the input file.\n"
        "The thinking process is as follows:\n"
        f"1. Determine the input data type of [harness_code] and analyze the input processing process in the code.\n"
        f"2. [slice_fun_code] is the {slice_fun} function code, and [sliced_forward_code] is the forward slice code of the {slice_fun} function. Combine [slice_fun_code] and [sliced_forward_code] to analyze the data flow and control flow of the {slice_fun} function, and generate the initial input that can cover the deeper path of the {slice_fun} function. Note: The initial input is for fuzz testing of the code, so the input must cover deeper paths and meet the input requirements on the one hand, and it must be easier to trigger vulnerabilities in the code on the other hand. \n"
        f"3. Generate a python code and write the input thought out in the previous step into the code. \n"
        f"4. Add a file writing module to the python code. The function of this module is to write the input written in the previous step into the target file after the python code is run. The file path to be written is {init_seed_file_path}. \n"
        f"[harness_code]:[{harness_code}] \n"
        f"[slice_fun_code]:[{slice_fun_code}]\n"
        f"[sliced_forward_code]:[{sliced_forward_code}]\n"
    )
    if flag is None:
        chain=rag_chain | init_seed_generate_codefile_parse2
    else:
        chain=rag_chain | init_seed_generate_codefile_parse
    response=RAG_chat(input_prompt,chain)
    return response


# Code to generate harness input file: file
def generate_init_seed_generate_file(sliced_forward_code,harness_code,slice_fun,slice_fun_code,ragchain,init_seed_file_path):

    encoded = tokenizer.encode(sliced_forward_code, add_special_tokens=False)
    truncated_tokens = encoded[:8000]
    sliced_forward_code=tokenizer.decode(truncated_tokens, skip_special_tokens=True)

    rag_chain=ragchain["rag_chain"]
    flag=ragchain["flag"]
    input_prompt = (
        f"Now you need to generate a python code. The purpose of the code is to generate the input file of [harness_code]. The generated file path is [{init_seed_file_path}]. The generated input file is used for subsequent fuzz testing of [harness_code]. It is necessary to ensure that the harness program can run correctly when using this input file.\n"
        "The thinking process is as follows:\n"
        f"1. Determine the input data type of [harness_code] and analyze the input processing process in the code.\n"
        f"2. [slice_fun_code] is the function code of {slice_fun}, and [sliced_forward_code] is the forward slice code of {slice_fun}. Combine [slice_fun_code] and [sliced_forward_code] to analyze the data flow and control flow of {slice_fun} function, and think out the initial input that can cover the deeper path of {slice_fun} function. Note: The initial input is for fuzz testing of the code, so the input should cover deeper paths and meet the input requirements on the one hand, and it should be easier to trigger vulnerabilities in the code on the other hand. \n"
        f"3. Generate a python code and call the generation library of related files according to the [harness_code] input type. Combine the related generation and processing functions of the files in the python library to generate the input thought out in the previous step. \n"
        f"4. Add an input file writing module in the python code to ensure that the initial input can be written into the target file after the python code is run. The generated initial input file path is {init_seed_file_path}. \n"
        f"[harness_code]:[{harness_code}] \n"
        f"[slice_fun_code]:[{slice_fun_code}]\n"
        f"[sliced_forward_code]:[{sliced_forward_code}]\n"
    )
    if flag is None:
        chain=rag_chain | init_seed_generate_codefile_parse2
    else:
        chain=rag_chain | init_seed_generate_codefile_parse
    response=RAG_chat(input_prompt,chain)
    return response
