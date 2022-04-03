from flask import *
from flask import render_template,redirect
from flask import Flask
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo
app = Flask(__name__)

myclient=pymongo.MongoClient("mongodb+srv://ayushmongo:Ayush13!@cluster0.ro4m7.mongodb.net/Hackathon?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
mydb=myclient['Hackathon']
mycol=mydb['Username']
mycol2=mydb['Data']

emissionsdata=[]

@app.route('/', methods=['GET','POST'])
def login():
  if request.method=='GET':
    return render_template('login.html')
  else:
    username=request.form['username']
    password=request.form['password']
    user=mycol.find_one({'Username': username, 'Password': password})
    if not user:
      flash('Email and password do not match')
      return redirect('/')
    else:
      print('home')
      return redirect('/home')

@app.route("/signup", methods=['GET','POST'])
def signup():
  if request.method=='GET':
    return render_template('signup.html')
  else:
    username1=request.form['username1']
    password1=request.form['password1']

    # if mycol.find_one({'Username': username1}):
    #   flash('Email already exists')
    #   return redirect('/')
    # print(username1)
    mycol.insert_one({'Username':username1, "Password":password1})
    return redirect('/logbook')

@app.route('/logbook', methods=['GET','POST'])
def log():
    if request.method=='GET':
        return render_template('logbook.html')
    else:
        milescar=request.form['milescar']
        milesbus=request.form['milesbus']
        milestrain=request.form['milestrain']
        massmeat=request.form['massmeat']
        massdairy=request.form['massdairy']
        energyconsumption=request.form['energyconsumption']
        naturalgas=request.form['naturalgas']
        family=request.form['family']
        personalspending=request.form['personalspending']
        emissionsdata.append(milescar)
        emissionsdata.append(milesbus)
        emissionsdata.append(milestrain)
        emissionsdata.append(massmeat)
        emissionsdata.append(massdairy)
        emissionsdata.append(energyconsumption)
        emissionsdata.append(naturalgas)
        emissionsdata.append(family)
        emissionsdata.append(personalspending)
        print('hi')

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/insights', methods=['GET','POST'])
def insights():
    if request.method=='GET':
      co2num=mycol2.find_one({'Car':emissionsdata[0]})
      return render_template('insights.html', mydata=co2num)
    else:
        milescar=int(request.form['milescar'])
        milesbus=int(request.form['milesbus'])
        milestrain=int(request.form['milestrain'])
        massmeat=int(request.form['massmeat'])
        massdairy=int(request.form['massdairy'])
        energyconsumption=int(request.form['energyconsumption'])
        naturalgas=int(request.form['naturalgas'])
        family=int(request.form['family'])
        personalspending=int(request.form['personalspending'])
        milescar=round(milescar/21.6*0.0089*907.2,2)
        milesbus=round((milesbus*0.06),2)
        milestrain=round((milesbus*0.15),2)
        totaltransport=(milesbus+milescar+milestrain)
        if massmeat==0:
            massmeat=0
        elif massmeat>=10:
            massmeat=round((massmeat*36),2)
        elif massmeat<10:
            massmeat=round((2.5*907.2),2)
        energyconsumption*=1.242*0.45/family
        energyconsumption=round(energyconsumption,2)
        naturalgas*=0.1196*0.45/family
        naturalgas=round(naturalgas,2)
        totalenergy=(energyconsumption+naturalgas)

        # mycol2.insert_one({'Car':milescar,'Bus':milesbus,'Train':milestrain,'TotalTransport':totaltransport})
        mycol2.insert_one({'Car':milescar,'Bus':milesbus,'Train':milestrain,'TotalTransport':totaltransport,'Meat':massmeat,'Energy':energyconsumption,'Gas':naturalgas,'TotalEnergy':totalenergy,'FamilySize':family,'PersonalSpending':personalspending,'Total':round((totaltransport+massmeat+totalenergy),2)})
        emissionsdata.append(milescar)
        emissionsdata.append(milesbus)
        emissionsdata.append(milestrain)
        emissionsdata.append(totaltransport)
        emissionsdata.append(massmeat)
        emissionsdata.append(massdairy)
        emissionsdata.append(energyconsumption)
        emissionsdata.append(naturalgas)
        emissionsdata.append(totalenergy)
        emissionsdata.append(family)
        emissionsdata.append(personalspending)
        print(emissionsdata)
        return redirect("/insights")
fig,ax=plt.subplots(figsize = (6,6))
ax = sns.set_style(style="darkgrid")
data = [
      ("Transportation",24),
      ("Diet",23),
      ("Household Enegy Consumption",43),
      ("Personal Consumption",23),
      ]
x = [row[0] for row in data]
y = [row[1] for row in data]

@app.route('/graph')
def graph():
      return render_template('graph.html')
      
@app.route('/visualize')  
def visualize():
      sns.lineplot(x,y)
      canvas=FigureCanvas(fig)
      img = io.BytesIO()
      fig.savefig(img)
      img.seek(0)
      return send_file(img,mimetype="img/png")
      
      

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)