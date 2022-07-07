## How to run parse?
1. Requirement: Python 3.9.x
2. Run **python setup.py**
3. Create a file **groupList.txt** contenting list of group links (for example: https://t.me/IoTLAB_Arduino_Group)
4. Run **python main.py**


## Algorithm:
1. Step 1: **getGroupLinks** from a file with a list of group links.
2. Step 2: **getGroupEntity** to get group Entity.
3. Step 3: **getGroupPosts** use the group Entity to get Posts in the time interval **fromTime to timeNow**.

## How to Develop with Python 3.9.7
1. Create a virtual environment: **python -m venv venv**
2. Activate the virtual enviroment.
3. Install the requirements: **pip install -r requirements.txt**
4. Create a file **groupList.txt** containing the group links.
5. Run parser: **python main.py**