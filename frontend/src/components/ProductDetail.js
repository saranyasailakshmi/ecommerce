import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

function ProductDetail() {
  const { id } = useParams(); // product id from URL
  const navigate = useNavigate();
  const accessToken = localStorage.getItem("access");

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const res = await api.get(`/product/${id}/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (res.data.success) {
        setProduct(res.data.data);
      } else {
        alert(res.data.message);
      }
      setLoading(false);
    } catch (err) {
      console.error(err);
      alert("Error fetching product");
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    try {
      // For simplicity, let's assume adding to cart is creating an order with 1 quantity
      const orderData = {
        total_amount: product.price,
        status: "pending",
        items: [{ product: product.id, quantity: 1 }],
      };
      const res = await api.post("/orders/create/", orderData, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (res.data.success) {
        alert("Product added to cart!");
      } else {
        alert(res.data.message);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to add to cart");
    }
  };

  const handleBuyNow = async () => {
    try {
      // Create order
      const orderData = {
        total_amount: product.price,
        status: "pending",
        items: [{ product: product.id, quantity: 1 }],
      };
      const orderRes = await api.post("/orders/create/", orderData, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (orderRes.data.success) {
        // Redirect to a payment page (optional)
        navigate(`/checkout/${orderRes.data.data.id}`);
      } else {
        alert(orderRes.data.message);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to buy product");
    }
  };

  if (loading) return <div className="container mt-5">Loading...</div>;
  if (!product) return <div className="container mt-5">Product not found</div>;

  return (
    <div className="container mt-5">
      <h2>{product.name}</h2>
      <div className="row">
        <div className="col-md-6">
          {product.images && product.images.length > 0 ? (
            <img
              src={`http://127.0.0.1:8000${product.images[0].image}`}
              alt={product.name}
              className="img-fluid"
            />
          ) : (
            <div>No image available</div>
          )}
        </div>
        <div className="col-md-6">
          <p>{product.description}</p>
          <p>
            <strong>Price:</strong> ₹{product.price}
          </p>
          <p>
            <strong>Stock:</strong> {product.quantity}
          </p>
          <p>
            <strong>Category:</strong> {product.category?.name || "N/A"}
          </p>
          <button className="btn btn-success me-2" onClick={handleBuyNow}>
            Buy Now
          </button>
          <button className="btn btn-primary" onClick={handleAddToCart}>
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
