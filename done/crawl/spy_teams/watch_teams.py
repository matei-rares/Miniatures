from pyppeteer import launch
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os 
from datetime import datetime

debug = False

current_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_path)
people_folder = os.path.join(current_directory, "people")
os.makedirs(people_folder, exist_ok=True)
#current_directory  is fullpath\current_directory

url="https://teams.microsoft.com/v2/?skipauthstrap=1"
 
sso_ext = current_directory + '\sso_extension'
print(sso_ext)
names = ['teams, name1','teams, name2']

peoples = []
for name in names:
    peoples.append({"name":name,"status":"Init"})

def extract_dynamic(in_url):
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir="/here",
                headless=False, #TODO set to false sometimes and log in if Unknown
                args=[
                    f"--disable-extensions-except={sso_ext}",
                    f"--load-extension={sso_ext}"
                    ])
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(in_url)
            page.wait_for_timeout(6000) # it takes a bit to load the page
            #page.screenshot(path="teams.png")
            
            refresh_interval = 60 * 1000  # Refresh every hour (in milliseconds)
            last_refresh_time = datetime.now()
            while True:
                print(f"{datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')} : Alive") 
                content = page.content()
                soup = BeautifulSoup(content,'html.parser')
                for people in peoples: 
                    old_status = people['status']
                    print(f"Checking {people['name']} , old status: {old_status}") if debug else None

                    people['status'] = find_status(soup,people['name'])
                    
                    print(f"New Status: {people['status']}") if debug else None
                    if people['status'] != old_status:
                        with open(people_folder+ f"/{people['name']}.txt", "a+", encoding="utf-8") as file:
                            # file.seek(0)
                            # lines = file.readlines()

                            # if len(lines) >= 2:
                            #     second_last_line = lines[-2].strip()
                            #     last_date = second_last_line.split(" : ")[0]
                            #     last_date_obj = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S").date()
                            #     current_date = datetime.now().date()
                            #     if last_date_obj and current_date != last_date_obj:
                            #         file.write("\n")

                            file.write(f"{datetime.now().strftime(f'%Y-%m-%d %H:%M:%S')} : {people['status']}\n")
        
                if (datetime.now() - last_refresh_time).total_seconds() * 1000 >= refresh_interval:
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Refreshing page")
                        page.reload()
                        page.wait_for_timeout(6000) 
                        last_refresh_time = datetime.now()


        except Exception as e:
            context.close()
            print("Error:", e)
       
    
def find_status(html_json,name):
    span = html_json.find('span', {'title': name, 'aria-label': name})
    print(f"Span: {span.prettify()}") if debug else None
    if span:
        status = span.find_parent().find_parent().find_parent().find('div',{'data-tid':'presence-badge'}).get('aria-label')
        return status
    # else:
    #     print(f"Element not found {span.prettify()}")

extract_dynamic(url)