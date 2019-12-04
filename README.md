# QWars

QWars is a qgame which is a quantum pygame to which we interface directly with the IBMQ Research HQ at the Thomas J. Watson Research Center in the cloud.  QWars is a shoot-em-up game where you, our hero, are flying the Q Ship which is armed with lasers to which various size lava rocks will be flying at you in addition to a REAL IBMQ quantum computer to which is chosen when we make the initial network call as it selects the least busy device to  to start the game.  The results of our quantum circuit will produce values between 1 and 200 to which almost half will go into 00 and the other half to 11.  There are 01 and 10 to account for noise.  We use these values to seed our randomizer to make a truly exciting and unique experience with each new game!  Our story is as follows.  Quantum supremacy has been achieved and an evil AI has taken control as they have manufactured thousands of deep-fake copies of our beloved quantum computers!  Your job as our hero is to shoot down the fake imposter quantum machines and save the universe from the AI singularity!

## OFFICIAL PRODUCT DEMO VIDEO

[youtube.com](https://youtu.be/3HdCAQinYOk/)

## Installation

Navigate to [python.org](https://www.python.org/downloads/) to install Python 3+.

Navigate to [git-scm.com](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git) to install Git.

Open a terminal window and type the below command to clone the GitHub QApp repo.

```bash
git clone https://github.com/mytechnotalent/qwars.git
cd qwars
```

With the terminal window open, type the below command to install all of the dependencies.

```bash
pip3 install -r requirements.txt
```

## Create and IBM Q Experience Account

Navigate to [quantum-computing.ibm.com](https://quantum-computing.ibm.com/) and create a new account.

Navigate to [quantum-computing.ibm.com/account](https://quantum-computing.ibm.com/account) and click the 'Copy token' button in blue to obtain your API.  Open up a text editor and paste in the token temporarily.

Open a terminal window and type the below command to setup your API key with your software.  Make sure you replace the 'MY_API_TOKEN' below with your API key you have stored in your text editor.  Be sure to paste the API key between the single quotes as shown below.

```python
python3
>>> from qiskit import IBMQ
>>> IBMQ.save_account('MY_API_TOKEN')
>>> quit()
```

## Run Application

With the terminal window open, type the below command to run your qapp.

```bash
python qwars.py
```

Navigate to [localhost:5000](http://localhost:5000) to launch your qapp in your default web browser.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0/)
