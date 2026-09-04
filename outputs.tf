output "dynamodb_table_name" {
  value = aws_dynamodb_table.tickets.name
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}
