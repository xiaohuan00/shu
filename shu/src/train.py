from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def train_model(train_data, model_name="THUDM/chatglm-6b"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # 实现微调逻辑
    return model 