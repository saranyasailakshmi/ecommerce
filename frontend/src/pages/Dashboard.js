import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Dashboard() {
  const navigate = useNavigate();
  const accessToken = localStorage.getItem("access");
  const user = localStorage.getItem("user");
  const role = localStorage.getItem("role");

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [editingProduct, setEditingProduct] = useState(null); // Track product being edited
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    quantity: "",
    category: "",
  });

  useEffect(() => {
    if (accessToken) {
      fetchProducts();
      fetchCategories();
    }
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await api.get("/product/list/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setProducts(res.data.data);

      const initialQuantities = {};
      res.data.data.forEach((p) => {
        initialQuantities[p.id] = 1;
      });
      setQuantities(initialQuantities);
    } catch (err) {
      console.error("Error fetching products:", err);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await api.get("/product/categories/list/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setCategories(res.data.data);
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  const handleQuantityChange = (productId, delta) => {
    setQuantities((prev) => {
      const newQty = Math.max(1, (prev[productId] || 1) + delta);
      return { ...prev, [productId]: newQty };
    });
  };

  const handleAddToCart = async (product) => {
    try {
      const quantity = quantities[product.id] || 1;
      await api.post(
        "/orders/create/",
        { items: [{ product_id: product.id, quantity }] },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      alert(`${quantity} item(s) added to cart!`);
    } catch (err) {
      console.error(err);
      alert("Failed to add product to cart");
    }
  };

  const handleBuyNow = async (product) => {
    try {
      const quantity = quantities[product.id] || 1;
      const orderRes = await api.post(
        "/orders/create/",
        { items: [{ product_id: product.id, quantity }] },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );

      const orderId = orderRes.data.data.id;
      const totalAmount = product.price * quantity;

      await api.post(
        "/orders/payments/create/",
        {
          order_id: orderId,
          amount: totalAmount,
          payment_method: "card",
        },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );

      alert(`Purchased ${quantity} item(s) successfully! Total: ₹${totalAmount}`);
    } catch (err) {
      console.error(err);
      alert("Failed to buy product");
    }
  };

  // ---------- EDIT PRODUCT ----------
  const handleEdit = (product) => {
    setEditingProduct(product.id);
    setFormData({
      name: product.name,
      description: product.description,
      price: product.price,
      quantity: product.quantity,
      category: product.category?.id || "",
    });
  };

  const handleUpdate = async () => {
    try {
      const res = await api.put(
        `/product/update/${editingProduct}/`,
        formData,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      alert("Product updated successfully!");
      setEditingProduct(null);
      fetchProducts();
    } catch (err) {
      console.error(err);
      alert("Failed to update product");
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/product/delete/${id}/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      alert("Product deleted successfully!");
      fetchProducts();
    } catch (err) {
      console.error(err);
      alert("Failed to delete product");
    }
  };

  if (!accessToken) {
    return (
      <div className="container mt-5">
        <h3>You are not logged in!</h3>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h2>Dashboard</h2>
      <p>
        Welcome, <strong>{user}</strong>! 
      </p>

      <div className="row">
        {products.map((product) => {
          const quantity = quantities[product.id] || 1;
          const totalPrice = product.price * quantity;

          return (
            <div className="col-md-4 mb-3" key={product.id}>
              <div className="card h-100">
                {product.images && product.images.length > 0 && (
                  <img
                    src={`http://127.0.0.1:8000${product.images[0].image}`}
                    alt={product.images[0].alt_text || product.name}
                    className="card-img-top"
                    style={{ height: "200px", objectFit: "cover" }}
                  />
                )}
                <div className="card-body">
                  {editingProduct === product.id ? (
                    // ---------- EDIT FORM ----------
                    <div>
                      <input
                        type="text"
                        className="form-control mb-2"
                        value={formData.name}
                        onChange={(e) =>
                          setFormData({ ...formData, name: e.target.value })
                        }
                        placeholder="Product Name"
                      />
                      <textarea
                        className="form-control mb-2"
                        value={formData.description}
                        onChange={(e) =>
                          setFormData({ ...formData, description: e.target.value })
                        }
                        placeholder="Description"
                      />
                      <input
                        type="number"
                        className="form-control mb-2"
                        value={formData.price}
                        onChange={(e) =>
                          setFormData({ ...formData, price: e.target.value })
                        }
                        placeholder="Price"
                      />
                      <input
                        type="number"
                        className="form-control mb-2"
                        value={formData.quantity}
                        onChange={(e) =>
                          setFormData({ ...formData, quantity: e.target.value })
                        }
                        placeholder="Quantity"
                      />
                      <select
                        className="form-control mb-2"
                        value={formData.category}
                        onChange={(e) =>
                          setFormData({ ...formData, category: e.target.value })
                        }
                      >
                        <option value="">Select Category</option>
                        {categories.map((c) => (
                          <option key={c.id} value={c.id}>
                            {c.name}
                          </option>
                        ))}
                      </select>

                      <button
                        className="btn btn-success btn-sm me-2"
                        onClick={handleUpdate}
                      >
                        Save
                      </button>
                      <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => setEditingProduct(null)}
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    // ---------- NORMAL VIEW ----------
                    <div>
                      <h5 className="card-title">{product.name}</h5>
                      <p className="card-text">{product.description}</p>
                      <p>Price: ₹{product.price}</p>

                      {role === "customer" && (
                        <div>
                          <div className="d-flex align-items-center mb-2">
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              onClick={() =>
                                handleQuantityChange(product.id, -1)
                              }
                            >
                              -
                            </button>
                            <span className="mx-2">{quantity}</span>
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              onClick={() =>
                                handleQuantityChange(product.id, 1)
                              }
                            >
                              +
                            </button>
                          </div>
                          <p>
                            <strong>Total: ₹{totalPrice}</strong>
                          </p>
                          <button
                            className="btn btn-primary btn-sm me-2"
                            onClick={() => handleAddToCart(product)}
                          >
                            Add to Cart
                          </button>
                          <button
                            className="btn btn-success btn-sm"
                            onClick={() => handleBuyNow(product)}
                          >
                            Buy Now
                          </button>
                        </div>
                      )}

                      {role === "seller" && (
                        <div>
                          <button
                            className="btn btn-warning btn-sm me-2"
                            onClick={() => handleEdit(product)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn btn-danger btn-sm"
                            onClick={() => handleDelete(product.id)}
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;
