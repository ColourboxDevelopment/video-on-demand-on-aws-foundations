#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { VodFoundation } from '../lib/vod-foundation-stack';
import {CbxAddition} from "../lib/cbx-additions-stack";

const branch = process.env.BUILD_BRANCH

if (branch == undefined || !(['master', 'development'].includes(branch))) {
    throw new Error(`"${branch}" is not a valid deployment target. Did you forget to set env var BUILD_BRANCH?`)
}
console.log(`building for "${branch}"`)

const DESTINATION_BUCKET_NAME = "claus-destination"
const API_HOST = ""
const STREAM_HOST = ""

const app = new cdk.App();

const base = new VodFoundation(DESTINATION_BUCKET_NAME, app, `streaming-defaults-${branch}`);

new CbxAddition(STREAM_HOST, API_HOST, base.getMediaConvertEndpoint(), base.getSnsTopic(), branch, app, `streaming-custom-${branch}`)