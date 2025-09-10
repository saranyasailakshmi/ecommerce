import React, { useEffect, useState } from "react";
import api from "../api";

function Products() {
  const [products, setProducts] = useState([]);
  const role = localStorage.getItem("role");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await api.get("/products/list/");
      setProducts(res.data.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/products/delete/${id}/`);
      alert("Product deleted!");
      fetchProducts();
    } catch (err) {
      alert("Error deleting product");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Products</h2>
      {role === "seller" && (
        <button className="btn btn-primary mb-3">+ Add Product</button>
      )}
      <div className="row">
        {products.map((product) => (
          <div className="col-md-4" key={product.id}>
            <div className="card mb-3">
              <div className="card-body">
                <h5 className="card-title">{product.name}</h5>
                <p className="card-text">{product.description}</p>
                <p>Price: ${product.price}</p>
                <p>Stock: {product.quantity}</p>
                <p>Category: {product.category?.name}</p>

                {/* Seller buttons */}
                {role === "seller" && (
                  <div>
                    <button className="btn btn-warning btn-sm me-2">Edit</button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(product.id)}
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Products;
