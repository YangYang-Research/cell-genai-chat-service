import boto3
import asyncio
from helpers.config import AppConfig, AWSConfig
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever

class RetrieverKB(object):
    def __init__(self):
        self.aws_conf = AWSConfig()
        self.bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=self.aws_conf.aws_region)

    async def general_knowledge_base(self, query: str) -> list[str]:
        def retrieve():
            retriever = AmazonKnowledgeBasesRetriever(
                client=self.bedrock_agent_runtime,
                knowledge_base_id=self.aws_conf.bedrock_knowledge_base_id,
                retrieval_config={"vectoerSearchConfiguration": {"numberOfResults": 5}},
            )
            contexts = retriever.invoke(input=query)
            return contexts
        return await asyncio.to_thread(retrieve)