# AWS IT Help Desk Platform

A beginner friendly help desk ticket demo. The **local demo** runs on your Windows computer and saves tickets in a small SQLite database. It does not need an AWS account and does not connect to AWS.

## Run it on Windows

1. On GitHub, open this repository and choose **Code → Download ZIP**.
2. In File Explorer, right-click the ZIP and choose **Extract All**.
3. Open the extracted `aws-it-helpdesk-platform-main` folder.
4. Click the address bar at the top of File Explorer, type `powershell`, and press **Enter**.
5. In PowerShell, run these commands one at a time:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe local_app.py
   ```

6. Leave PowerShell open. In Chrome, visit **http://127.0.0.1:5001**.
7. To stop the demo, return to PowerShell and press **Ctrl+C**.

Port **5001** keeps this demo separate from the IT Resilience Command Center, which uses port 5000.

The demo starts with one sample VPN ticket. Create a ticket, open it from the list, and change its status. Your demo tickets are saved in `instance/helpdesk.sqlite3` inside the project folder. This is sample data on your computer.

## Run the checks

From the extracted project folder, open PowerShell and run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests check that the page loads, a ticket can be created, its status can be changed, and an unknown ticket returns a not found page.

## How this relates to AWS

The project also includes an AWS Lambda ticket handler, a health check, and Terraform files. Those files are **not a complete AWS deployment** yet: the current Terraform does not create the Lambda functions or API Gateway, and the Lambda code has not been verified against a live AWS account. Do not run `terraform apply` expecting a working cloud service.

The local demo is a separate, working prototype that helps you learn the ticket workflow without AWS credentials or cloud charges. Deploying the AWS version will require completing and testing the cloud infrastructure in an AWS account.

## Example ticket

```json
{
  "title": "VPN connection issue",
  "description": "User cannot connect to the corporate VPN",
  "priority": "High",
  "requester": "user@example.com"
}
```

## Technologies

- Python and Flask for the local demo
- SQLite for local ticket storage
- AWS Lambda, DynamoDB, IAM, and Terraform starter files for future cloud deployment
