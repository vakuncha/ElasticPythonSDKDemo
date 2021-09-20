import os
import datetime
from azure.identity import ClientSecretCredential
from azure.mgmt.elastic import MicrosoftElastic
from azure.mgmt.elastic.models import *

credentials = ClientSecretCredential(
        client_id=os.environ.get("AZURE_CLIENT_ID"),
        client_secret=os.environ.get("AZURE_CLIENT_SECRET"),
        tenant_id=os.environ.get("AZURE_TENANT_ID"),
    )

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = os.environ["AZURE_RESOURCE_GROUP"]

elastic_client = MicrosoftElastic(credentials, 
subscription_id)

monitor_result = elastic_client.monitors.list_by_resource_group("vakuncha-test-rg")

print(f"List All Elastic resource")

while (x := next(monitor_result, None)) is not None:
    print(x.name)

monitor_result = elastic_client.monitors.list_by_resource_group("vakuncha-test-rg")
resource_tobe_deleted = next(monitor_result, None)

if(resource_tobe_deleted is not None):
    print(f"Deleting Resource {resource_tobe_deleted.name}")
    elastic_client.monitors.begin_delete("vakuncha-test-rg",resource_tobe_deleted.name).result()



resource_name = "PythonSDKCreate-"+ str(int(datetime.datetime.now().timestamp()))

print(f"Creating Resource {resource_name}")

monitor_properties = MonitorProperties()

monitor_properties.user_info = UserInfo(first_name ="varun",last_name = "kunchakuri",company_name="microsoft",email_address="sdkdemo@mpliftrelastic20210901outlo.onmicrosoft.com")

monitor_properties.user_info.company_info = CompanyInfo(domain = "software",business = "cloud",country = "india",state="andhrapradesh")


monitor_resource = ElasticMonitorResource(properties = monitor_properties,location = "eastus2euap",sku=ResourceSku(name = "ess-monthly-consumption_Monthly"))


elastic_client.monitors.begin_create("vakuncha-test-rg",resource_name,monitor_resource).result()


