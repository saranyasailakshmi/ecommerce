import React, { useEffect, useState } from "react";
import api from "../api";

function Orders() {
  const [orders, setOrders] = useState([]);
  const accessToken = localStorage.getItem("access");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const res = await api.get("/orders/list/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setOrders(res.data.data);
    } catch (err) {
      console.error("Error fetching orders:", err);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Your Orders</h2>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <ul className="list-group">
          {orders.map((order) => (
            <li className="list-group-item" key={order.id}>
              <strong>Order #{order.id}</strong> - {order.status} - ₹{order.total_amount}
              <ul>
                {order.items.map((item) => (
                  <li key={item.id}>
                    {item.product?.name || "Unknown Product"} × {item.quantity} = ₹{item.total_price}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Orders;
