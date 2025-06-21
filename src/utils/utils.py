# 通用工具类
import os
import yaml
import requests, json
import logging

logger = logging.getLogger(__name__)


def get_memory_dir():
    """Get the directory of the memory file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    memory_dir = os.path.join(base_dir, "../", "memory")
    return memory_dir


def get_config():
    """获取配置"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir, "../config", "configs.yaml")
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"读取配置文件失败: {str(e)}")
        return {}


def get_log_dir():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
    return log_dir


def request_qwen(model_name, system_instruction, prompt):
    config = get_config()
    qwen_config = config.get("qwen_client", {})
    max_tokens = qwen_config.get("max_tokens", 8000)
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_instruction

            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        "stream": "false",
        "temperature": 0,
        # "top_p": 1,
        "max_tokens": max_tokens
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {get_config()['friday_client']['api_key']}"
    }
    response = requests.post(get_config()['friday_client']['base_url'] + '/chat/completions', json=payload,
                             headers=headers, timeout=3600)
    # print(response.text)
    if response.status_code == 200:
        result = response.json()
        if result['choices']:
            return (result['choices'][0]['message']['content'])
        else:
            return response.text
    else:
        return (f'Error: {response.text}')


def store_to_vector_db(vector_data):
    """
    存储数据到向量数据库
    Args:
        vector_data (dict): 要存储的向量数据
    Returns:
        bool: 是否存储成功
    """
    try:
        print(f"向量数据库存储数据: {vector_data}")
        response = requests.post(get_config()["learning"]["write_vector_store"]["url"], json=vector_data)
        response.raise_for_status()
        result = response.json()
        if result.get('code') == 0:
            # data 可能是字符串，需要先解析
            data = result.get('data')
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception:
                    print(f"返回的data字段无法解析为JSON: {data}")
                    return False
            if data.get('success') is True:
                return True
            else:
                print(f"写入失败: {data.get('msg', '未知错误')}")
                return False
        else:
            print(f"请求失败: {result.get('message', '未知错误')}")
            return False
    except Exception as e:
        print(f"向量数据库存储失败: {str(e)}")
        return False
