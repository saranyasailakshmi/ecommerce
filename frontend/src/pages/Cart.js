// import React, { useEffect, useState } from "react";
// import api from "../api";

// function Cart() {
//   const [cartItems, setCartItems] = useState([]);
//   const accessToken = localStorage.getItem("access");

//   // Fetch cart items on load
//   useEffect(() => {
//     fetchCart();
//   }, []);

//   const fetchCart = async () => {
//     try {
//       const res = await api.get("/cart/", {
//         headers: { Authorization: `Bearer ${accessToken}` },
//       });
//       setCartItems(res.data.data || []);
//     } catch (err) {
//       console.error("Error fetching cart:", err);
//     }
//   };

//   // Remove an item from the cart
//   const handleRemove = async (itemId) => {
//     try {
//       await api.delete(`/cart/${itemId}/delete/`, {
//         headers: { Authorization: `Bearer ${accessToken}` },
//       });
//       fetchCart(); // refresh cart
//     } catch (err) {
//       console.error("Error removing item:", err);
//     }
//   };

//   return (
//     <div className="container mt-5">
//       <h2>Your Cart</h2>
//       {cartItems.length === 0 ? (
//         <p>No items in your cart.</p>
//       ) : (
//         <ul className="list-group">
//           {cartItems.map((item) => (
//             <li className="list-group-item d-flex justify-content-between align-items-center" key={item.id}>
//               <div>
//                 <strong>{item.product?.name}</strong> <br />
//                 {item.quantity} × ₹{item.product?.price} = ₹
//                 {item.quantity * item.product?.price}
//               </div>
//               <button
//                 className="btn btn-danger btn-sm"
//                 onClick={() => handleRemove(item.id)}
//               >
//                 Remove
//               </button>
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );
// }

// export default Cart;

import React, { useEffect, useState, useCallback } from "react";
import api from "../api";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const accessToken = localStorage.getItem("access");

  // ✅ useCallback prevents warning
  const fetchCart = useCallback(async () => {
    try {
      const res = await api.get("/cart/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setCartItems(res.data.data || []);
    } catch (err) {
      console.error("Error fetching cart:", err);
    }
  }, [accessToken]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const handleRemove = async (itemId) => {
    try {
      await api.delete(`/cart/${itemId}/delete/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      fetchCart();
    } catch (err) {
      console.error("Error removing item:", err);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Your Cart</h2>
      {cartItems.length === 0 ? (
        <p>No items in your cart.</p>
      ) : (
        <ul className="list-group">
          {cartItems.map((item) => (
            <li
              className="list-group-item d-flex justify-content-between align-items-center"
              key={item.id}
            >
              <div>
                <strong>{item.product?.name}</strong> <br />
                {item.quantity} × ₹{item.product?.price} = ₹
                {item.quantity * item.product?.price}
              </div>
              <button
                className="btn btn-danger btn-sm"
                onClick={() => handleRemove(item.id)}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Cart;
