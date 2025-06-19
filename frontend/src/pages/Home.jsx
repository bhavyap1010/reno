import { useState, useEffect } from "react"
import api from "../api"
import ServiceRequest from "../components/ServiceRequest"
import "../styles/Home.css"

function Home() {
    const [serviceRequests, setServiceRequests] = useState([])
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")

    useEffect(() => {
        getServiceRequests();
    }, [])

    const getServiceRequests = () => {
        api
          .get("/api/service-requests/")
          .then((response) => response.data)
          .then((data) => setServiceRequests(data))
          .catch((error) => alert(error));
    }

    const deleteServiceRequest = (id) => {
        api
          .delete(`/api/service-requests/delete/${id}/`)
          .then((response) => {
            if (response.status === 204) alert("Request deleted.");
            else alert("Failed to delete request.");
            getServiceRequests();
          })
          .catch((error) => alert(error));
    }

    const createServiceRequest = (e) => {
        e.preventDefault()
        api
          .post("/api/service-requests/", { title, description })
          .then((response) => {
            if (response.status === 201) alert("Request created.");
            else alert("Failed to create request.");
            getServiceRequests();
          })
          .catch((error) => alert(error));
    }

    return (
        <div>
            <div>
                <h2>Service Requests</h2>
                {serviceRequests.map((serviceRequest) => (
                    <ServiceRequest serviceRequest={serviceRequest} onDelete={deleteServiceRequest} key={serviceRequest.id} />
                ))}
            </div>

            <h2> Post a Service Request </h2>
            <form onSubmit={createServiceRequest}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="description">Description:</label>
                <br />
                <textarea
                    id="description"
                    name="description"
                    required
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home