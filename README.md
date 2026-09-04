# 🛠️ AWS IT Help Desk Platform

> **Serverless IT operations platform built with AWS Lambda, DynamoDB, IAM, API Gateway concepts, CloudWatch, Python, and Terraform.**

## Why I built this

IT support teams need more than a ticket form: they need reliable persistence, controlled access, observable services, and automation. This project models the backend of a lightweight help desk platform using AWS managed services.

## Architecture

```text
User / Support Tool
        |
        v
   API Gateway
        |
        v
     Lambda
      /   \
     v     v
DynamoDB  CloudWatch Logs
```

## Core capabilities

- Create IT support tickets
- Retrieve tickets by ID
- Persist ticket metadata in DynamoDB
- Apply an IAM role with scoped DynamoDB permissions
- Emit operational logs to CloudWatch
- Add a health-check Lambda for service verification
- Provision foundational resources with Terraform
- Validate behavior with Python tests

## Example ticket

```json
{
  "title": "VPN connection issue",
  "description": "User cannot connect to the corporate VPN",
  "priority": "High",
  "requester": "user@example.com"
}
```

## Engineering decisions

**Serverless:** Lambda removes server management for a small event-driven workload.

**DynamoDB:** A key-value/document model fits ticket lookup by `TicketId` and avoids unnecessary database administration.

**IAM:** The Lambda role is restricted to the DynamoDB operations it needs rather than granting broad administrator access.

**Observability:** CloudWatch logging provides a starting point for operational troubleshooting.

## Skills demonstrated

AWS Lambda · DynamoDB · IAM · CloudWatch · REST/API concepts · Terraform · Python · JSON · troubleshooting · serverless architecture

## What I would improve for production

- API Gateway resource/method definitions
- Authentication and authorization
- AWS WAF and throttling
- Structured JSON logging
- CloudWatch alarms and dashboards
- Dead-letter handling
- Encryption and key-management strategy
- CI/CD deployment with GitHub Actions
- Integration and load testing

## Portfolio note

This repository is intended as a demonstrable cloud engineering project. For a production claim, deploy it in an AWS account and add screenshots plus the deployment details to this README.
