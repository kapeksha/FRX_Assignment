The project is divided into three main components:
 
1. **Task Manager**
2. **Authentication**
3. **Proto Files**


### Installation
 
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

 ### Running the Project
 
1. Apply the database migrations:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
2. Start the authentication gRPC server:
   ```bash
   python auth_server.py
   ```
3. Start the task_project application:
   ```bash
   flask run
   ```
3. Start the auth_project application:
   ```bash
   flask run
   ```
   
## Usage
 
- Use the authentication APIs to register, login, and manage user profiles.
- Use the Task Manager APIs to create, update, and manage tasks, projects, and comments.
