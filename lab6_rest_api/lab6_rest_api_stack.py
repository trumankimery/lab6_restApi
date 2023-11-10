import json, aws_cdk
from aws_cdk import (
    # Duration,
    Stack,
    Size,
    aws_apigateway as apigateway,
    # aws_sqs as sqs,
)
from constructs import Construct

class Lab6RestApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the API Gateway
        api = apigateway.RestApi(self, "ProductsApi",
            rest_api_name='Products API',
            description='API to get all the food products.',
            min_compression_size=Size.bytes(123),
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            ),
            deploy_options={
                'stage_name': 'dev'
            }
        )

        method_response = apigateway.MethodResponse(
            status_code='200',
            response_parameters={
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Origin': True,
                'method.response.header.Access-Control-Allow-Methods': True
            },
            response_models={
                'application/json': apigateway.Model.EMPTY_MODEL
            }
        )
        integration_response = apigateway.IntegrationResponse(
            status_code='200',
            response_parameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'GET'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            },
            response_templates={
                "application/json": json.dumps({
                    "product_item_arr": [
                        {
                            "product_name_str": "apple pie slice",
                            "product_id_str": "a444",
                            "price_in_cents_int": 595,
                            "description_str":"amazing taste",
                            "tag_str_arr": ["pie slice","on offer"],
                            "special_int": 1
                        },{
                            "product_name_str": "chocolate cake slice",
                            "product_id_str": "a445",
                            "price_in_cents_int": 595,
                            "description_str":"chocolate heaven",
                            "tag_str_arr": ["cake slice","on offer"]
                        },{
                            "product_name_str": "chocolate cake",
                            "product_id_str": "a446",
                            "price_in_cents_int": 4095,
                            "description_str": "chocolate heaven",
                            "tag_str_arr": ["whole cake", "on offer"]
                        }
                    ]
                })
            },
        )
        api.root.apply_removal_policy = aws_cdk.RemovalPolicy.DESTROY

        products = api.root.add_resource('products')
        products.add_method(
            'GET',
            integration=apigateway.MockIntegration(
                integration_responses=[integration_response],

                request_templates={
                    'application/json': '{"statusCode": 200}'
                }
            ),
            method_responses=[method_response]
        )



        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Lab6RestApiQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
