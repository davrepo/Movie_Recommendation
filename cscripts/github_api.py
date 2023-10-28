import numpy as np
import requests
from envvars import GITHUB_TOKEN
from datetime import date
from time import time
import os
import sys
import json
from tqdm import tqdm
from pprint import pprint

local_path = os.path.dirname(os.path.realpath(__file__))
if local_path not in sys.path:
    sys.path.append(local_path)


class Markdown:

    def __init__(self) -> None:
        self.header = f"# Repository overview\nCreated: {date.today().strftime('%d/%m/%y')}\n\nComputation Time: [comp_time] sec\n"
        self.content = f"""{self.header}\n"""

    def add_section_title(self, title):
        self.content += f"## {title}\n---\n"

    def add_repo_section(self, title, repo):

        self.add_section_title(title)

        if repo:
            self.content += f"""**Description**\n\n{repo.description}\n\n**Homepage**\n\n{repo.homepage}\n\n**Key highlights**\n\n- Number of watches: {repo.watchers_count}\n\n- Number of forks: {repo.forks_count}\n\n- Star gazers count: {repo.stargazers_count}\n\n- Open issues count: {repo.open_issues_count}\n\n- Topics: {repo.topics}\n\n- Has a wiki: {repo.has_wiki}\n\n- Language: {repo.language}\n\n"""
        else:
            self.content += """An error occured when fetching data from api.\n"""


class Repo:

    def __init__(self, data) -> None:

        # No meta?
        self.has_meta = len(data) > 0

        # If meta, parse relevant
        if self.has_meta:
            # * Relevant attributes
            self.name = data.get("name") if data.get('name') else None
            self.description = data.get("description") if data.get('description') else None
            self.forks_count = data.get("forks_count") if data.get('forks_count') else None
            self.stargazers_count = data.get("stargazers_count") if data.get('stargazers_count') else None
            self.watchers_count = data.get("watchers_count") if data.get('watchers_count') else None
            self.open_issues_count = data.get("open_issues_count") if data.get('open_issues_count') else None
            self.topics = set(data.get("topics")) if data.get('topics') else None
            self.has_wiki = data.get("has_wiki") if data.get('has_wiki') else None
            self.languages = {x[0] for x in data.get("languages")} if data.get('languages') else None
            self.homepage = data.get("homepage") if data.get('homepage') else None


class GithubApi:

    def __init__(self, token) -> None:
        self.token = token

    def get_repo_data(self, repo_name):
        """
        Returns raw repo metda data.
        :repo_name: [owner_name]/[actual_repo_name], str
        :return: status_code, dict
        """
        #print("="*10)
        #print(f"Fetching data from Github API for: {repo_name}\n")
        # Define parameters
        owner, repo = repo_name.split("/")

        # Define query
        query_url = f"https://api.github.com/repos/{owner}/{repo}"

        # Define headers
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}

        # Send a request
        r = requests.get(query_url, headers=headers)

        # Return proper response
        if r.status_code == 200:
            #print(self.get_error_response(r.status_code))
            #print("="*10)
            return r.status_code, r.json()

        else:
            #print(self.get_error_response(r.status_code))
            #print("="*10)
            return r.status_code, dict()

    def get_error_response(self, status_code):
        """
        Returns an appropriate response based on provided status_code.
        :status_code: int
        :return: str  
        """

        if status_code == 401:
            return "Access denied. Probably invalid token."
        elif status_code == 200:
            return "Request successful."
        else:
            return "Unknown error."


class ReposSummary(GithubApi):

    def __init__(self, token=GITHUB_TOKEN, repositories=[], name='unknown', path='.') -> None:

        # Inherit from the parent class
        super().__init__(token)

        # Define this class' properties
        self.repositories = repositories
        self.path = path  # where to save the summary
        self.name = name
        self.given_meta = None

        # Run the neccesary functions
        self.load_given_metadata()

    def load_given_metadata(self):
        """
        Loads and saves as attribute given metadata.
        """

        # Load metadata which we have from the dataset
        with open("../data/transformed/metadata.json", "r") as f:

            # Load it
            metadata = json.load(f)

            # Adjust it so you have repo name as a key
            metadata = {values["repo_name"]
                : values for values in metadata.values()}

        # Save it
        self.given_meta = metadata

    def generate_summary(self):

        print("="*10)
        print("Started summary generation")
        print("="*10 + "\n")

        # Measure the computation
        start = time()

        # Save the data to a string
        M = Markdown()

        for repo_name in self.repositories:

            # Fetch data from API
            repo = self.get_relevant_repo_info(repo_name)

            # Add it to the markdown
            M.add_repo_section(repo_name, repo)

        end = time()

        # Add computational time
        M.content = M.content.replace(
            "[comp_time]", f"{round(end - start, 2)}")

        # Save it
        with open(f'{self.path}/{self.name}.md', 'w') as outfile:
            outfile.write(M.content)

    def get_relevant_repo_info(self, repo_name):
        """
        Returns selected info about repo.
        :repo_name: str
        :return: None or Repo object
        """

        # API metadata
        status, info = self.get_repo_data(repo_name)

        # Combine the results into a dictionary
        # If there is no metadata at all, it will yield empty dict
        if status == 200:
            combined = info  # to unite the terminology for next ops
            combined.update(self.given_meta.get(repo_name, dict()))
        else:
            combined = self.given_meta.get(repo_name, dict())

        # Select relevant data
        r = Repo(combined)

        return r


"""
def get_all_metadata(repos, filepath='.', name='api_metadata.json'):
    api = GithubApi(GITHUB_TOKEN)

    # random_sample = np.random.choice(list(recommendations.keys()), size=int(len(recommendations)*test_size)) 

    attributes = ['topics']
    with open('../data/transformed/

    data = {} 
    for repo in repos:
        res = api.get_repo_data(repo)[1]
        key = res.get('full_name')
        val = {attribute: res.get(attribute) for attribute in attributes}
        val.update

        data[key] = val
        print(data)
        break


"""
if __name__ == '__main__':
    with open('./untitled.json', 'r') as infile:
        data = json.load(infile)
    repos = data.keys()

    api = GithubApi(GITHUB_TOKEN)

    c = 0
    for repo in tqdm(repos):
        status_code, res = api.get_repo_data(repo)

        if res.get('topics'):
            print(res.get('topics'))
            c+=1
            if c==100:
                break


    



