locals {
    lambda_name = "${var.project}-${var.environment}-dothething"
    # Include the resource type that will use this role
    iam_role_name = "${var.project}-${var.environment}-lambda-dothething"
}


resource "aws_iam_role" "iam_for_lambda" {
  name = "iam-for-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = merge(local.tags, {Name=local.iam_role_name})
}




data "archive_file" "init" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda.py"
  output_path = "${path.module}/lambda/lambda.zip"
}



resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda/lambda.zip"
  function_name = local.lambda_name
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda.handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = data.archive_file.init.output_base64sha256

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }

  tags = merge(local.tags, {Name=local.lambda_name})
}