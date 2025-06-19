import React from "react";
import "../styles/ServiceRequest.css"

function ServiceRequest({ serviceRequest, onDelete }) {
    const formattedDate = new Date(serviceRequest.created_at).toLocaleDateString("en-US")

    return (
        <div className="request-container">
            <p className="request-title">{serviceRequest.title}</p>
            <p className="request-content">{serviceRequest.description}</p>
            <p className="request-date">{formattedDate}</p>
            <button className="delete-button" onClick={() => onDelete(serviceRequest.id)}>
                Delete
            </button>
        </div>
    );
}

export default ServiceRequest