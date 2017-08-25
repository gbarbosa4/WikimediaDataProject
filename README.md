<img src="https://github.com/LiquidGalaxyLAB/WikimediaDataProject/blob/master/static/img/logos/logo_WDLGV.png" width="250">

# WikiData Liquid Galaxy Visualization | WDLGV

The WDLGV project has the purpose of showing some data in Liquid Galaxy. This information is obtained from Wikidata, who acts as central storage for the structured data in Wikimedia projects.
The visulaization is represented in Liquid Galaxy sistem, and the information appears in a bubble and different shapes. There are also the possibility to generate a tour that shows the place and starts an orbit around it. 
The user has at his disposal five options to select and the user experience is funny, interesting and easy.

##  Installing

Follow step by step instructions for installing the project

#### 1. Clone this repository
  
    git clone https://github.com/gbarbosa4/WikimediaDataProject.git
    
#### 2. Go to the new project folder
  
    cd WikimediaDataProject

#### 3. Create VirtualEnv with python

    virtualenv -p python [VirtualEnv Folder Name]

#### 4. Install some system requirements

    sudo apt-get install libffi-dev libssl-dev python3-dev
    
#### 5. Activate VirtualEnv

    source [VirtualEnv Folder Name]/bin/activate

#### 6. Install project requirements (this step could take some time)

    pip install -r requirements.txt

#### 7. Run Django

    ./WDLG-Start [Liquid Galaxy IP]

#### 8. Go to Web Application ( in your navegator )

    http://[Your IP]:8000


##  Built with

    · Python3   · Django    · Material Design


## Licensing

[MIT License](../master/LICENSE) - Copyright (c) 2017 Guillem Barbosa Costa
     
