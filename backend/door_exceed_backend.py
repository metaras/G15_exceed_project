from flask import Flask, request
from flask_pymongo import PyMongo
import time
from flask_cors import cross_origin
import json


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group15:qt63ba2n@158.108.182.0:2255/exceed_group15'
mongo = PyMongo(app)

myCollection = mongo.db.mall_A
myCollection1 = mongo.db.time_A
myCollectionB = mongo.db.mall_B
myCollection2 = mongo.db.time_B
myCollectionHA = mongo.db.hardware_A
myCollectionHB = mongo.db.hardware_B
myCollectionLA = mongo.db.lastest_A
myCollectionLB = mongo.db.lastest_B
myCollectionYA = mongo.db.time_A_yesterday
myCollectionYB = mongo.db.time_B_yesterday
mall_A_yesterday = mongo.db.mall_A_yesterday
mall_B_yesterday = mongo.db.mall_B_yesterday
time_A_average = mongo.db.time_A_average
time_B_average = mongo.db.time_B_average

@app.route('/in',methods=['POST'])
def In():
    x = request.json
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7

    mall_yesterday()
    if (x["mall"] == "A"):
        flit = {"name": "cumming_in"}
        query = myCollection.find_one(flit)
        myIn = query["in"]
        # x = request.json
        update = {"$set": {"in": int(myIn + 1)}}
        myCollection.update_one(flit, update)
    if (x["mall"] == "B"):
        flit = {"name": "cumming_in"}
        query = myCollectionB.find_one(flit)
        myIn = query["in"]
        # x = request.json
        update = {"$set": {"in": int(myIn + 1)}}
        myCollectionB.update_one(flit, update)
    temp()
    people()
    update_people()
    time_average()
    return {'result': 'Updated successfully'}

@app.route('/out',methods=['POST'])
def Out():
    x = request.json
    if (x["mall"] == "A"):
        flit = {"name": "cumming_out"}
        query = myCollection.find_one(flit)
        myOut = query["out"]
        #x = request.json
        update={"$set": {"out": int(myOut+1)}}
        myCollection.update_one(flit,update)
    if (x["mall"] == "B"):
        flit = {"name": "cumming_out"}
        query = myCollectionB.find_one(flit)
        myOut = query["out"]
        # x = request.json
        update = {"$set": {"out": int(myOut + 1)}}
        myCollectionB.update_one(flit, update)
    people()
    update_people()
    time_average()
    return {'result': 'Updated successfully'}

@app.route('/people',methods=['POST'])
def people():
    x = request.json
    if (x["mall"] == "A"):
        flit = {"name": "people&density"}

        filt_in = myCollection.find_one({"name": "temp"})
        myIn=filt_in["pass"]

        filt_out = myCollection.find_one({"name": "cumming_out"})
        myOut = filt_out["out"]

        update_content = {"density": float((int(myIn) - int(myOut)) / 10),"people":int(myIn) - int(myOut)}

        update = {"$set":update_content}
        myCollection.update_one(flit, update)
    if (x["mall"] == "B"):
        flit = {"name": "people&density"}

        filt_in = myCollectionB.find_one({"name": "temp"})
        myIn = filt_in["pass"]

        filt_out = myCollectionB.find_one({"name": "cumming_out"})
        myOut = filt_out["out"]

        update_content = {"density": float((int(myIn) - int(myOut)) / 10), "people": int(myIn) - int(myOut)}

        update = {"$set": update_content}
        myCollectionB.update_one(flit, update)
    return {'result': 'Updated successfully'}

@app.route('/update_people',methods=['POST'])
def update_people():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    x = request.json
    if (x["mall"] == "A"):
        f_lastest={"name": "lastest_A"}
        query=myCollectionLA.find_one(f_lastest)
        lastest_A=query["lastest"]
        if(lastest_A>hr):
            for i in range (10,22):
                i=str(i)
                filt_last={"start": i}
                query_la=myCollection1.find_one(filt_last)
                l=query_la["people"]
                l_out = query_la["out"]
                l_in = query_la["in"]
                update={"$set": {"people": int(l),"in":int(l_in),"out":int(l_out)}}
                reset = {"$set": {"people": 0,"in":0,"out":0}}
                myCollectionYA.update_one(filt_last, update)
                myCollection1.update_one(filt_last, reset)
        flit1 = {"name": "temp"}
        query1 = myCollection.find_one(flit1)
        myIn = query1["pass"]
        flit2 = {"name": "cumming_out"}
        query2 = myCollection.find_one(flit2)
        myOut = query2["out"]
        flit3 = {"name": "cumming_in"}
        query3 = myCollection.find_one(flit3)
        myIn3 = query3["in"]

        flit = {"start": str(hr)}
        f_lastest_a = {"name": "lastest_A"}
        update_la = {"$set": {"lastest": hr}}
        update = {"$set": {"people": int(int(myIn) - int(myOut)),
                           "in":int(myIn),
                           "out":int(myOut)}}
        myCollection1.update_one(flit,update)
        myCollectionLA.update_one(f_lastest_a, update_la)
    if (x["mall"] == "B"):
        f_lastest = {"name": "lastest_B"}
        query = myCollectionLB.find_one(f_lastest)
        lastest_B = query["lastest"]
        if (lastest_B > hr):
            for i in range(10, 22):
                i = str(i)
                filt_last = {"start": i}
                query_lb = myCollection2.find_one(filt_last)
                l = query_lb["people"]
                l_in = query_lb["in"]
                l_out = query_lb["out"]
                update = {"$set": {"people": int(l),"in":int(l_in),"out":int(l_out)}}
                reset={"$set": {"people": 0,"in":0,"out":0}}
                myCollectionYB.update_one(filt_last, update)
                myCollection2.update_one(filt_last, reset)
        flit1 = {"name": "temp"}
        query1 = myCollectionB.find_one(flit1)
        myIn = query1["pass"]
        flit2 = {"name": "cumming_out"}
        query2 = myCollectionB.find_one(flit2)
        myOut = query2["out"]
        flit3 = {"name": "cumming_in"}
        query3 = myCollectionB.find_one(flit3)
        myIn3 = query3["in"]

        flit = {"start": str(hr)}
        f_lastest_b = {"name": "lastest_B"}
        update = {"$set": {"people": int(int(myIn) - int(myOut)),
                           "in": int(myIn),
                           "out": int(myOut)}}
        update_lb = {"$set": {"lastest": hr }}
        myCollection2.update_one(flit, update)
        myCollectionLB.update_one(f_lastest_b,update_lb)
    return {'result': 'Updated successfully'}

@app.route('/temp',methods=['POST'])
def temp():
    x = request.json
    if (x["mall"] == "A"):
        temp=x["temp"]
        flit = {"name": "temp"}
        query = myCollection.find_one(flit)
        Pass=query["pass"]
        not_Pass=query["not_pass"]
        total=Pass+not_Pass+1
        if(temp<=37.5):
            update = {"$set": {"pass": int(Pass)+1,"total":total}}
        else:
            update = {"$set": {"not_pass": int(not_Pass) + 1,"total":total}}
        myCollection.update_one(flit, update)
    if (x["mall"] == "B"):
        temp = x["temp"]
        flit = {"name": "temp"}
        query = myCollectionB.find_one(flit)
        Pass = query["pass"]
        not_Pass = query["not_pass"]
        total = Pass + not_Pass + 1
        if (temp <= 37.5):
            update = {"$set": {"pass": int(Pass) + 1, "total": total}}
        else:
            update = {"$set": {"not_pass": int(not_Pass) + 1, "total": total}}
        myCollectionB.update_one(flit, update)
    return {'result': 'Updated successfully'}

@app.route('/mall_yesterday',methods=['POST'])
def mall_yesterday():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    x = request.json
    f_in = {"name": "cumming_in"}
    f_out = {"name": "cumming_out"}
    f_people = {"name": "people&density"}
    f_temp = {"name": "temp"}
    if (x["mall"] == "A"):
        f_lastest = {"name": "lastest_A"}
        query = myCollectionLA.find_one(f_lastest)
        lastest_A = query["lastest"]
        if (lastest_A > hr):
            q_in=myCollection.find_one(f_in)
            y_in=q_in["in"]
            u_in={"$set": {"in": y_in }}
            mall_A_yesterday.update_one(f_in,u_in)
            u_in_reset={"$set": {"in": 0}}
            myCollection.update_one(f_in,u_in_reset)

            q_out=myCollection.find_one(f_out)
            y_out=q_out["out"]
            u_out = {"$set": {"out": y_out}}
            mall_A_yesterday.update_one(f_out,u_out)
            u_out_reset = {"$set": {"out": 0}}
            myCollection.update_one(f_out, u_out_reset)

            q_people=myCollection.find_one(f_people)
            y_people=q_people["people"]
            y_density=q_people["density"]
            u_people = {"$set": {"people": y_people,"density":y_density}}
            mall_A_yesterday.update_one(f_people, u_people)
            u_people_reset={"$set": {"people": 0,"density":0}}
            myCollection.update_one(f_people, u_people_reset)

            q_temp=myCollection.find_one(f_temp)
            y_pass=q_temp["pass"]
            y_notpass=q_temp["not_pass"]
            y_total=q_temp["total"]
            u_temp = {"$set": {"pass": y_pass,"not_pass": y_notpass,"total":y_total}}
            mall_A_yesterday.update_one(f_temp, u_temp)
            u_temp_reset={"$set": {"pass": 0,"not_pass": 0,"total":0}}
            myCollection.update_one(f_temp, u_temp_reset)

    if (x["mall"] == "B"):
        f_lastest = {"name": "lastest_B"}
        query = myCollectionLB.find_one(f_lastest)
        lastest_B = query["lastest"]
        if (lastest_B > hr):
            q_in=myCollectionB.find_one(f_in)
            y_in=q_in["in"]
            u_in={"$set": {"in": y_in }}
            mall_B_yesterday.update_one(f_in,u_in)
            u_in_reset = {"$set": {"in": 0}}
            myCollectionB.update_one(f_in, u_in_reset)

            q_out=myCollectionB.find_one(f_out)
            y_out=q_out["out"]
            u_out = {"$set": {"out": y_out}}
            mall_B_yesterday.update_one(f_out,u_out)
            u_out_reset = {"$set": {"out": 0}}
            myCollectionB.update_one(f_out, u_out_reset)

            q_people=myCollectionB.find_one(f_people)
            y_people=q_people["people"]
            y_density=q_people["density"]
            u_people = {"$set": {"people": y_people,"density":y_density}}
            mall_B_yesterday.update_one(f_people, u_people)
            u_people_reset = {"$set": {"people": 0, "density": 0}}
            myCollectionB.update_one(f_people, u_people_reset)

            q_temp=myCollectionB.find_one(f_temp)
            y_pass=q_temp["pass"]
            y_notpass=q_temp["not_pass"]
            y_total=q_temp["total"]
            u_temp = {"$set": {"pass": y_pass,"not_pass": y_notpass,"total":y_total}}
            mall_B_yesterday.update_one(f_temp, u_temp)
            u_temp_reset = {"$set": {"pass": 0, "not_pass": 0, "total": 0}}
            myCollectionB.update_one(f_temp, u_temp_reset)

@app.route('/time_average',methods=['POST'])
def time_average():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    x = request.json
    if (x["mall"] == "A"):
        for i in range (10,22):
            i=str(i)
            f={"start":i}
            q_today=myCollection1.find_one(f)
            p_today=q_today["people"]
            q_yesterday=myCollectionYA.find_one(f)
            p_yesterday=q_yesterday["people"]
            avg=(p_today+p_yesterday)/2
            update={"$set":{"people":avg}}
            time_A_average.update_one(f,update)
    if (x["mall"] == "B"):
        for i in range (10,22):
            i = str(i)
            f={"start":str(i)}
            q_today=myCollection2.find_one(f)
            p_today=q_today["people"]
            q_yesterday=myCollectionYB.find_one(f)
            p_yesterday=q_yesterday["people"]
            avg=(p_today+p_yesterday)/2
            update={"$set":{"people":avg}}
            time_B_average.update_one(f,update)
    return {"result":1}

@app.route('/get_dens_A',methods = ['GET'])
@cross_origin()
def get_dens_A():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"people&density"}
    q=myCollection.find_one(f)
    people=q["people"]
    dens=q["density"]
    y=mall_A_yesterday.find_one(f)
    people_y=y["people"]
    dens_y=y["density"]
    return {"people":people,
            "density":dens,
            "people_yesterday":people_y,
            "density_yesterday":dens_y,
            "hour":hr,
            "minute":m}

@app.route('/get_dens_B',methods = ['GET'])
@cross_origin()
def get_dens_B():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"people&density"}
    q=myCollectionB.find_one(f)
    people=q["people"]
    dens=q["density"]
    y=mall_B_yesterday.find_one(f)
    people_y=y["people"]
    dens_y=y["density"]
    return {"people":people,
            "density":dens,
            "people_yesterday":people_y,
            "density_yesterday":dens_y,
            "hour":hr,
            "minute":m}

@app.route('/get_in_A',methods = ['GET'])
@cross_origin()
def get_in_A():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"cumming_in"}
    q=myCollection.find_one(f)
    myIn=q["in"]
    y = mall_A_yesterday.find_one(f)
    myIn_yesterday=y["in"]
    return {"in":myIn,"in_yesterday":myIn_yesterday,
            "hour":hr,
            "minute":m}

@app.route('/get_in_B',methods = ['GET'])
@cross_origin()
def get_in_B():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"cumming_in"}
    q=myCollectionB.find_one(f)
    myIn=q["in"]
    y = mall_B_yesterday.find_one(f)
    myIn_yesterday = y["in"]
    return {"in": myIn, "in_yesterday": myIn_yesterday,
            "hour":hr,
            "minute":m}

@app.route('/get_out_A',methods = ['GET'])
@cross_origin()
def get_out_A():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"cumming_out"}
    q=myCollection.find_one(f)
    myOut=q["out"]
    y = mall_A_yesterday.find_one(f)
    myOut_yesterday=y["out"]
    return {"out":myOut,"out_yesterday":myOut_yesterday,
            "hour":hr,
            "minute":m}

@app.route('/get_out_B',methods = ['GET'])
@cross_origin()
def get_out_B():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f={"name":"cumming_out"}
    q=myCollectionB.find_one(f)
    myOut=q["out"]
    y = mall_B_yesterday.find_one(f)
    myOut_yesterday=y["out"]
    return {"out":myOut,"out_yesterday":myOut_yesterday,
            "hour":hr,
            "minute":m}

@app.route('/get_temp_A',methods = ['GET'])
@cross_origin()
def get_temp_A():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f = {"name": "temp"}
    q = myCollection.find_one(f)
    myPass=q["pass"]
    myNotPass=q["not_pass"]
    myTotal=q["total"]
    y = mall_A_yesterday.find_one(f)
    myPass_y = y["pass"]
    myNotPass_y = y["not_pass"]
    myTotal_y = y["total"]
    return {"pass":myPass,"not_pass":myNotPass,"total":myTotal,
            "pass_yesterday":myPass_y,
            "not_pass_yesterday":myNotPass_y,
            "total_yesterday":myTotal_y,
            "hour":hr,
            "minute":m}

@app.route('/get_temp_B',methods = ['GET'])
@cross_origin()
def get_temp_B():
    named_tuple = time.localtime()  # get struct_time
    time_hr = time.strftime("%-H", named_tuple)
    hr = int(time_hr) + 7
    m = int(time.strftime("%-M", named_tuple))

    f = {"name": "temp"}
    q = myCollectionB.find_one(f)
    myPass=q["pass"]
    myNotPass=q["not_pass"]
    myTotal=q["total"]
    y = mall_B_yesterday.find_one(f)
    myPass_y = y["pass"]
    myNotPass_y = y["not_pass"]
    myTotal_y = y["total"]
    return {"pass": myPass, "not_pass": myNotPass, "total": myTotal,
            "pass_yesterday": myPass_y,
            "not_pass_yesterday": myNotPass_y,
            "total_yesterday": myTotal_y,
            "hour":hr,
            "minute":m}

@app.route('/get_time_A',methods = ['GET'])
@cross_origin()
def get_time_A():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=myCollection1.find_one(f)
        people=q["people"]
        myIn=q["in"]
        myOut=q["out"]
        b={str(i):{"people":people,
                   "in":myIn,
                   "out":myOut}}
        a.update(b)
    return a

@app.route('/get_time_A_yesterday',methods = ['GET'])
@cross_origin()
def get_time_A_yesterday():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=myCollectionYA.find_one(f)
        people=q["people"]
        myIn = q["in"]
        myOut = q["out"]
        b = {str(i): {"people": people,
                      "in": myIn,
                      "out": myOut}}
        a.update(b)
    return a

@app.route('/get_time_A_average',methods = ['GET'])
@cross_origin()
def get_time_A_averagey():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=time_A_average.find_one(f)
        people=q["people"]
        b={str(i):people}
        a.update(b)
    return a

@app.route('/get_time_B',methods = ['GET'])
@cross_origin()
def get_time_B():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=myCollection2.find_one(f)
        people=q["people"]
        myIn = q["in"]
        myOut = q["out"]
        b = {str(i): {"people": people,
                      "in": myIn,
                      "out": myOut}}
        a.update(b)
    return a

@app.route('/get_time_B_yesterday',methods = ['GET'])
@cross_origin()
def get_time_B_yesterday():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=myCollectionYB.find_one(f)
        people=q["people"]
        myIn = q["in"]
        myOut = q["out"]
        b = {str(i): {"people": people,
                      "in": myIn,
                      "out": myOut}}
        a.update(b)
    return a

@app.route('/get_time_B_average',methods = ['GET'])
@cross_origin()
def get_time_B_averagey():
    a = {}
    for i in range (10,22):
        f={"start":str(i)}
        q=time_B_average.find_one(f)
        people=q["people"]
        b={str(i):people}
        a.update(b)
    return a

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='2255', debug=True)

