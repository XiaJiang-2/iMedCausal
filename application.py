from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import numpy as np
import networkx
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename


import iRCT
import PC
import rFCI
import FGES
import FCI
import GES


application = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx', 'dat'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/", methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")

@application.route("/iRCTHome", methods=['GET', 'POST'])
def iRCTHome():

    if request.method == 'GET':
        error = ''
        if request.args.get('error', None) != None:
            error = request.args.get('error', None)
        
        return render_template("iRCT_Home.html", error=error)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect("/iRCTHome")
        f = request.files['file']
        data_path = 'datasets/' + secure_filename(f.filename)
        delim = request.form['delim']
        functionNum = request.form['functionNum']
        if f and allowed_file(f.filename):
            f.save(data_path)
            uploaded_file = True
            return redirect(url_for('iRCT_Page', filename=data_path, uploaded_file=uploaded_file, delim=delim, functionNum = functionNum))
        else:
            return redirect("/iRCTHome")
        
@application.route("/iRCT", methods=['GET', 'POST'])
def iRCT_Page():
    if request.method == 'GET':
        file_uploaded = bool(request.args.get('uploaded_file', None))
        if file_uploaded == True:
            filename = request.args.get('filename', None)
            delim = request.args.get('delim', None)


            df = pd.read_csv(filename, sep=delim)
            listOfColumns = df.columns

            return render_template("iRCT_Page.html", name=filename, columns=listOfColumns, delim=delim, functionNum=request.args.get('functionNum', None))
        else:
            return redirect('/iRCTHome')
    
    if request.method == 'POST':
        treatmentCol = request.form['treat_column']
        outcomeCol = request.form['out_column']
        functionNum = request.form['functionNum']
        
        if functionNum == "4":
            covariateCol = request.form['covariate_column']
        else:
            covariateCol = None
        fileName = request.form['fileName']
        delimiter = request.form['delimiter']


        df = pd.read_csv(fileName, sep=delimiter)
        df.index = range(1, len(df)+1, 1)

        if treatmentCol == outcomeCol or treatmentCol == covariateCol or outcomeCol == covariateCol:
            errMsg = 'Two of the columns cannot be the same.'
            # os.remove(fileName)
            return redirect(url_for('iRCTHome', error=errMsg))
        else:
            myiRCT = iRCT.iRCT(df, treatmentCol, outcomeCol, functionNum, covariateCol)
            # os.remove(fileName)
            return render_template("iRCT_Output.html", result=str(myiRCT.relationVal), outcome=outcomeCol, treatment=treatmentCol)
        

@application.route("/CausalLearnHome", methods=['GET', 'POST'])
def causalLearnHome():
    if request.method == 'GET':
        return render_template("CausalLearn_Home.html")
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect("/CausalLearnHome")
        f = request.files['file']
        data_path = 'datasets/' + secure_filename(f.filename)
        if f and allowed_file(f.filename):
            f.save(data_path)
            uploaded_file=True
            return redirect(url_for('CausalLearn_Page', filename=data_path, uploaded_file=uploaded_file))
        else:
            return redirect("/CausalLearnHome")
        
@application.route("/causalLearn", methods=['GET', 'POST'])
def CausalLearn_Page():
    if request.method == 'GET':
        file_uploaded = bool(request.args.get('filename', None))
        if file_uploaded == True:
            filename = request.args.get('filename', None)

            return render_template("CausalLearn_Page.html", name=filename)
        else:
            return redirect('/CausalLearnHome')
    
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        fileName = request.form['fileName']

        if algorithm == "PC":
            return redirect(url_for("PC_Page", name=fileName))

        if algorithm == "rFCI":
            return redirect(url_for("rFCI_Page", name=fileName))
        
        if algorithm == "FGES":
            return redirect(url_for("FGES_Page", name=fileName))
        
        if algorithm == "GES":
            return redirect(url_for("GES_Page", name=fileName))
        
        if algorithm == "FCI":
            return redirect(url_for("FCI_Page", name=fileName))
        
@application.route("/PC", methods=['GET'])
def PC_Page():
    if request.method == 'GET':
        fileName = request.args.get('name', None)
        # pcObject = PC.PC(fileName)
        # os.remove(fileName)
        # adjArray = np.array(pcObject.output)
        # G = networkx.from_numpy_array(adjArray, create_using=networkx.DiGraph)
        # networkx.draw(G)
        # plt.savefig("PC_Output.png")
        return render_template("PC.html", Lines=pcObject.output)
    
@application.route("/rFCI", methods=['GET', 'POST'])
def rFCI_Page():
    if request.method == 'GET':
        fileName = request.args.get('name', None)

        return render_template("rFCI.html", name=fileName)
    if request.method == 'POST':
        fileName = request.form['fileName']
        delimiter = request.form['delim']

        rfciObject = rFCI.rFCI(fileName, delimiter, "templates/rFCI_Outputs", "rFCI_Result")
        f = open("templates/rFCI_Outputs/rFCI_Result.txt", 'r')
        rFCI_Data = f.readlines()
        f.close()
        # os.remove(fileName)
        return render_template("rFCI_Output.html", Lines=rFCI_Data)

@application.route("/FGES", methods=['GET', 'POST'])
def FGES_Page():
    if request.method == 'GET':
        fileName = request.args.get('name', None)

        return render_template("FGES.html", name=fileName)

    if request.method == 'POST':
        fileName = request.form['fileName']
        delimiter = request.form['delim']

        fgesObject = FGES.FGES(fileName, delimiter, "templates/FGES_Outputs", "FGES_Result")
        f = open("templates/FGES_Outputs/FGES_Result.txt", 'r')
        FGES_Data = f.readlines()
        f.close()
        # os.remove(fileName)
        return render_template("FGES_Output.html", Lines=FGES_Data)
    
@application.route("/FCI", methods=['GET', 'POST'])
def FCI_Page():
    if request.method == 'GET':
        fileName = request.args.get('name', None)

        return render_template("FCI.html", name=fileName)

    if request.method == 'POST':
        fileName = request.form['fileName']
        delimiter = request.form['delim']

        df = pd.read_csv(fileName, sep=delimiter)

        fciObject = FCI.FCI(df, "static/images/FCI_Output.png")
        # os.remove(fileName)
        return render_template("FCI_Output.html")

@application.route("/GES", methods=['GET', 'POST'])
def GES_Page():
    if request.method == 'GET':
        fileName = request.args.get('name', None)

        return render_template("GES.html", name=fileName)

    if request.method == 'POST':
        fileName = request.form['fileName']
        delimiter = request.form['delim']

        df = pd.read_csv(fileName, sep=delimiter)

        gesObject = GES.GES(df, "static/images/GES_Output.png")
        # os.remove(fileName)
        return render_template("GES_Output.html")

if __name__ == "__main__":
    application.run(debug=True)
