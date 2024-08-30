"""
_summary_
"""
import pinecone_pulumi as pinecone
import pulumi_aws as aws

def declare_pinecone_resources():
    """_summary_
    """
    # Create the Pinecone index
    pinecone.PineconeIndex(
        'games',
        name='games',
        metric=pinecone.IndexMetric.COSINE,
        dimension=1536,
        spec=pinecone.PineconeSpecArgs(
            serverless=pinecone.PineconeServerlessSpecArgs(
                cloud=pinecone.ServerlessSpecCloud.AWS,
                region=aws.Region.US_WEST2,
            ),
        ),
    )
