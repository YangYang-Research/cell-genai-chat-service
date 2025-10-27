import boto3
from langchain_aws import ChatBedrockConverse
from helpers.config import AppConfig, AWSConfig

class Model():
    def __init__(self):
        self.aws_conf = AWSConfig()
        self.bedrock_client = boto3.client("bedrock-runtime", region_name=self.aws_conf.aws_region)

    def claude_model_text(self):
        model = ChatBedrockConverse(
            client=self.bedrock_client,
            model=self.aws_conf.bedrock_model_claude_text_id,
            temperature=self.aws_conf.bedrock_model_claude_text_temperature,
            max_tokens=self.aws_conf.bedrock_model_claude_text_max_tokens
        )
        return model
    
    def claude_model_vision(self):
        model = ChatBedrockConverse(
            client=self.bedrock_client,
            model=self.aws_conf.bedkrock_model_claude_vision_id,
            temperature=self.aws_conf.bedrock_model_claude_vision_temperature,
            max_tokens=self.aws_conf.bedrock_model_claude_vision_max_tokens
        )
        return model