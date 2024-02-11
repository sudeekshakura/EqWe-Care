const express = require('express');
const { MongoClient, ObjectId } = require('mongodb');
const cors = require('cors');

const app = express();
app.use(cors()); // Use the cors middleware

const port = 3001;

const uri = "mongodb+srv://kura:Elnino123456789@cluster0.afwuy4j.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

app.get('/data', async (req, res) => {
  try {
    await client.connect();
    const database = client.db("Gtech");
    const collection = database.collection("Gtech");
    const queryResult = await collection.find({}).toArray();
    res.json(queryResult);
  } catch (error) {
    console.error("Error fetching data from MongoDB:", error);
    res.status(500).json({ error: "Internal server error" });
  } finally {
    await client.close();
  }
});

app.get('/data/:id', async (req, res) => {
  try {
    const id = req.params.id;
    await client.connect();
    const database = client.db("Gtech");
    const collection = database.collection("Gtech");
    const queryResult = await collection.findOne({ "seqn": parseInt(id) });
    res.json(queryResult);
  } catch (error) {
    console.error("Error fetching data from MongoDB:", error);
    res.status(500).json({ error: "Internal server error" });
  } finally {
    await client.close();
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
