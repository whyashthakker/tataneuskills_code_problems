## Pushing Code to GitHub Repository

1. Initialize a Git repository (if not already done):
   ```
   git init
   ```

2. Add all files to the staging area:
   ```
   git add .
   ```

3. Commit the changes:
   ```
   git commit -m "Initial commit"
   ```

4. Create a new repository on GitHub:
   - Go to GitHub.com and sign in
   - Click the '+' icon in the top right and select 'New repository'
   - Name your repository and click 'Create repository'

5. Link your local repository to the GitHub repository:
   ```
   git remote add origin https://github.com/yourusername/your-repo-name.git
   ```

6. Push your code to GitHub:
   ```
   git push -u origin master
   ```

   Note: If your main branch is named 'main' instead of 'master', use:
   ```
   git push -u origin main
   ```

## Setting up Virtual Environment and Installing Requirements

1. Navigate to your project directory:
   ```
   cd path/to/your/project
   ```

2. Create a virtual environment:
   - On macOS and Linux:
     ```
     python3 -m venv myenv
     ```
   - On Windows:
     ```
     python -m venv myenv
     ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     myenv\Scripts\activate
     ```

4. Your prompt should change to indicate the virtual environment is active.

5. Install requirements from requirements.txt:
   ```
   pip install -r requirements.txt
   ```

6. You're now ready to work on your project with all the required packages installed.

7. When you're done, you can deactivate the virtual environment:
   ```
   deactivate
   ```

Remember to activate your virtual environment each time you work on your project.

