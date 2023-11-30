# TRIPS & TIPS BLOG
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![PyTest](https://img.shields.io/badge/Pytest-003A9B?style=for-the-badge&logo=pytest&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

Trips & Tips is a Django-based blog designed for adventurers to share their experiences with fellow travelers.

## Features

### Account Management

* **Create Account:** Easily register and become a part of the Trips & Tips community.
* **Change Password:** Securely update your password whenever needed.
* **Delete Account:** Delete your account whenever you decide.

### Profile Discovery

* **Automated Profile Creation:** Your profile is automatically generated during registration.
* **Edit Profile:** Customize your profile by updating your profile picture and providing a brief description about yourself.
* **Explore Profiles:** Visit other users' profiles to discover more about them and explore the posts they've created.

### Blogging

* **Create & Edit Posts:** Share your adventures by creating engaging posts. Edit and refine your content, ensuring it reflects your adventures perfectly.
* **Publish or Save as Draft:** Choose to publish your posts for others to see or save them as drafts for future editing and publishing.

### Explore Engaging Content

* **Read Others' Posts:** Discover a variety of travel stories and experiences shared by fellow users.
* **Commenting:** Engage with the community by leaving comments on posts that inspire you.


### Efficient Tag-Based Searching

* **Search by Tags:** Easily navigate posts by clicking on tags or using the search bar to find content related to specific themes or topics.

## Installation

Follow these steps to set up Trips & Tips on your local machine:

1. **Clone the Repository:** Download the project by running the following command in your terminal:
```
git clone https://github.com/kamilakokoszka/Trips_and_tips
```
2. **Create a Virtual Environment:** Navigate to the project directory and create a virtual environment:
```
python -m venv venv
```
3. **Activate the Virtual Environment:** Activate the virtual environment based on your operating system:
- On Windows:
    ```shell
    venv\Scripts\activate
    ```
- On macOS/Linux:
  ```shell
  source venv/bin/activate
  ```
4. **Install Required Packages:** Install the project dependencies by running:
```
pip install -r requirements.txt
```
5. **Set Up Environment Variables:** Update the `settings.py` file with appropriate values for the following variables:
- `SECRET_KEY`
- `DATABASES`: Update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_PORT` and comment `DB_URL`

6. **Run the Application:** Start the development server by executing the following command:
```
python manage.py runserver
```
7. **Access the Application:** Open your web browser and navigate to http://localhost:8000/.

