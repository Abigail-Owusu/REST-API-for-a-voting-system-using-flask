import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# prompt 1
@app.route("/register_voter", methods=["POST"])
def register_voter():
    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400

    record = json.loads(request.data)
    with open("./tmp/data_voters.txt", "r") as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)

        # check if user is already registered
        for voter in records:
            if voter["id"] == record["id"]:
                return jsonify({"error": "This voter has already been registered"}), 400
        records.append(record)
    with open("./tmp/data_voters.txt", "w") as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)


# prompt 2
@app.route("/deregister_voter/<id_number>", methods=["DELETE"])
def deregister_voter(id_number):
    with open("./tmp/data_voters.txt", "r") as file:
        data = json.load(file)

    # Remove voter with matching ID number from data
    for i in range(len(data)):
        if data[i]["id"] == id_number:
            data.pop(i)
            break
        else:
            return (
                jsonify(
                    {
                        "Message": f"Voter with ID number {id_number} is not in the records and so can not be deleted"
                    }
                ),
                404,
            )

    # Save updated data to file
    with open("./tmp/data_voters.txt", "w") as file:
        json.dump(data, file)

    # Return success message
    return (
        jsonify(
            {
                "Message": f"Voter with ID number {id_number} has been successfully deregistered."
            }
        ),
        204,
    )


# prompt 3
@app.route("/update_voter/<id_number>", methods=["PUT"])
def update_voter_details(id_number):
    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400
    record = json.loads(request.data)
    new_records = []
    with open("./tmp/data_voters.txt", "r") as f:
        data = f.read()
        records = json.loads(data)
    for voter in records:
        if voter["id"] == id_number:
            # Update voter information based on request data
            voter["name"] = record["name"]
            voter["year"] = record["year"]
            voter["major"] = record["major"]
        else:
            return (
                jsonify(
                    {
                        "error": f"This ID number,{id_number}, does not represent any student"
                    }
                ),
                404,
            )
        new_records.append(voter)
    with open("./tmp/data_voters.txt", "w") as f:
        f.write(json.dumps(new_records, indent=2))

    return jsonify(record), 201


# prompt 4
@app.route("/get_voter/<id_number>", methods=["GET"])
def get_voter_data(id_number):
    with open("./tmp/data_voters.txt", "r") as f:
        data = f.read()
        voters = json.loads(data)
    for voter in voters:
        if voter["id"] == id_number:
            return voter
    return (
        jsonify(
            {"error": f"This ID number,{id_number}, does not represent any student"}
        ),
        404,
    )


# prompt 5


@app.route("/create_elections", methods=["POST"])
def create_election():
    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400
    record = json.loads(request.data)
    with open("./tmp/data_elections.txt", "r") as f:
        data = f.read()
    record["voters"] = []
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        # check if the type of election is already registered
        for election in records:
            if election["id"] == record["id"]:
                return (
                    jsonify(
                        {
                            "error": f"This {election['name']} election has already been registered"
                        }
                    ),
                    400,
                )
        records.append(record)
    with open("./tmp/data_elections.txt", "w") as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record), 201


# prompt 6
@app.route("/get_election/<id_number>", methods=["GET"])
def get_election_data(id_number):
    with open("./tmp/data_elections.txt", "r") as f:
        data = f.read()
        elections = json.loads(data)
    for voter in elections:
        if voter["id"] == id_number:
            return voter
    return (
        jsonify(
            {"error": f"This ID number,{id_number}, does not represent any election"}
        ),
        404,
    )


# prompt 7
@app.route("/delete_election/<id_number>", methods=["DELETE"])
def delect_election(id_number):
    with open("./tmp/data_elections.txt", "r") as file:
        data = json.load(file)

    # Remove voter with matching ID number from data
    for i in range(len(data)):
        if data[i]["id"] == id_number:
            data.pop(i)
            break
        else:
            return f"Election id does not exist", 404

    # Save updated data to file
    with open("./tmp/data_elections.txt", "w") as file:
        json.dump(data, file)

    # Return success message
    return f"Election has been successfully deleted.", 204


# prompt 8
@app.route("/elections/<id_number>/vote", methods=["POST"])
def vote_in_election(id_number):
    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400
    vote = json.loads(request.data)

    # check if voter been registered
    with open("./tmp/data_voters.txt", "r") as f:
        data = f.read()
        voter_details = json.loads(data)
    is_registered = False
    for voter in voter_details:
        if voter["id"] == vote["voter_id"]:
            is_registered = True
            break

    if not is_registered:
        return (
            jsonify({"error": "You are not registered to vote in this election :("}),
            404,
        )

    with open("./tmp/data_elections.txt", "r") as f:
        data = f.read()
        elections = json.loads(data)

    for election in elections:
        if election["id"] == id_number:
            # Check if the voter has voted
            if vote["voter_id"] in election["voters"]:
                return (
                    jsonify({"error": "You have already voted in this election."}),
                    400,
                )
            else:
                # Add the vote to the candidate's vote count
                for candidate in election["candidates"]:
                    if candidate["id"] == vote["candidate_id"]:
                        candidate["vote_count"] += 1

                        # add the particular voter to the list of voters
                        election["voters"].append(vote["voter_id"])

                        with open("./tmp/data_elections.txt", "w") as f:
                            f.write(json.dumps(elections, indent=2))
                        return jsonify({"success": "Your vote has been counted."}), 201
    return jsonify({"error": "Election not found."}), 404


app.run(debug=True)
