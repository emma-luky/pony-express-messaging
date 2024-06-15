import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [joinDate, setJoinDate] = useState("");
  const [readOnly, setReadOnly] = useState(true);

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
      const formattedJoinDate = new Date(user.created_at).toDateString();
      setJoinDate(formattedJoinDate);
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("username: " + username);
    console.log("email: " + email);
    console.log("join date: " + joinDate);
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="flex flex-col max-w-96 mx-auto px-4 py-8 justify-center">
      <h2 className="text-2xl font-bold py-2">
        Details
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
        <FormInput
          name="Username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="Email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />
        <FormInput
          name="Member Since"
          type="email"
          value={joinDate}
          readOnly={readOnly}
          setter={setJoinDate}
        />
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }
        <Button type="button" onClick={onClick}>
          {readOnly ? "edit" : "cancel"}
        </Button>
      </form>
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;