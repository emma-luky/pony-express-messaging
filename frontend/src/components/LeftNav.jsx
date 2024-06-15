import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useApi } from "../hooks";

const emptyChat = (id) => ({
  id,
  name: "loading...",
  empty: true,
});

function Link({ chat }) {
  const url = chat.empty ? "#" : `/chats/${chat.id}`;
  const className = ({ isActive }) => [
    "p-2",
    "hover:bg-slate-800 hover:text-grn",
    "flex flex-row justify-between",
    isActive ?
      "bg-slate-800 text-grn font-bold" :
      ""
  ].join(" ");

  const chatName = ({ isActive }) => (
    (isActive ? "\u00bb " : "") + chat.name
  );

  return (
    <NavLink to={url} className={className}>
      {chatName}
    </NavLink>
  );
}

function LeftNav() {
  const [search, setSearch] = useState("");
  const api = useApi();

  const { data } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      api.get("/chats")
        .then((response) => response.json())
    ),
  });

  const regex = new RegExp(search.split("").join(".*"));

  const chats = ( data?.chats || [1, 2, 3].map(emptyChat)
  ).filter((chat) => (
    search === "" || regex.test(chat.name)
  ));

  return (
    <nav className="flex flex-col h-[650px]">
      <div className="flex flex-col overflow-y-scroll h-full">
        {chats.map((chat) => (
          <Link key={chat.id} chat={chat} />
        ))}
      </div>
    </nav>
  );
}

export default LeftNav;