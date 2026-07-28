import { useEffect, useState } from "react";

export function UserList({ fetchUsers, onSelect }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers().then(setUsers);
  }, []);

  return (
    <ul>
      {users.map((u, i) => (
        <li key={i} onClick={() => onSelect(u)}>
          {u.name}
        </li>
      ))}
    </ul>
  );
}

export function Bio({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
