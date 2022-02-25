# AWS::SAM::ApiAuthValidator

CloudFormation hook for enforcing that all paths and methods in the OpenApi definition have an authorizer attached.

Intrinsic functions are resolved before the hook.

## Valid:
```json
{
	"Body": {
		"components": {
			"securitySchemes": {
				"MyLambdaAuthUpdated": {
					...
				}
			}
		},
		"openapi": "3.0",
		"paths": {
			"/post": {
				"post": {
					"x-amazon-apigateway-integration": {
						"payloadFormatVersion": "1.0",
						"httpMethod": "POST",
						"type": "aws_proxy",
						"uri": "..."
					},
                    "security": [
                        {
                            "MyLambdaAuthUpdated": []
                        }
                    ]
				}
			}
		},
		"info": {
			...
		}
	}
}
```

## Invalid:
```json
{
	"Body": {
		"components": {
			"securitySchemes": {
				"MyLambdaAuthUpdated": {
					...
				}
			}
		},
		"openapi": "3.0",
		"paths": {
			"/post": {
				"post": {
					"x-amazon-apigateway-integration": {
						"payloadFormatVersion": "1.0",
						"httpMethod": "POST",
						"type": "aws_proxy",
						"uri": "..."
					}
				}
			}
		},
		"info": {
			...
		}
	}
}
```