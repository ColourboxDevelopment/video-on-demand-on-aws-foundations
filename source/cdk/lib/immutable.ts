import * as cdk from 'aws-cdk-lib';
import { ApiKey } from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs'

export class StreamingImmutable extends cdk.Stack {

    apiKey: ApiKey

    constructor(branch: string, scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props)

        this.apiKey = new ApiKey(this, `streaming_api_key_${branch}`, {
            apiKeyName: `streaming_api_key_${branch}`,
            description: `Key used for all ${branch} streaming endpoints`
        })
    }

    public getApiKey(): ApiKey
    {
        return this.apiKey
    }
}
