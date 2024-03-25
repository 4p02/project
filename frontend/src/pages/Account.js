const Account = () => {
  const list = ["Change Password", "Delete Account"];

  return (
    <div className="page">
      <h1 className="title">Account Settings</h1>
      <div className="panel w-2/3 first:border-t-0 last:border-b-0 *:mt-1 p-0">
        {list.map( (txt, index) =>
          <div key={index} className="text-center text-lg w-full h-fit border-col border-2">
            {txt}
          </div>
        )}
      </div>
    </div>
  )
}
export default Account