interface LinkProps {
  text: string; 
  url:string;
}

function MyLink(props: LinkProps) {
  return (
  <>
  <button className="text-[40px] text-black  text-center mt-[30px] bg-white p-[6px] w-[200px] border-[2px] border-black">
  <a href={props.url}> { props.text}</a> 
  </button>
  </>

  )

}




export default function Home() {
  return (
    <div>
      <main className="w-full">
          <div className="text-white 	text-center">
          <div className="text-[65px] mt-[100px]">WELCOME TO</div>
          <h1 className="text-[175px] mt-[15px]">EmergenSee</h1>
          <div className="text-[90px] mt-[15px] italic">Safety in Sight</div>
        </div>
        <div className="flex flex-col items-center mt-[30px]">
         <MyLink url="/About" text="ABOUT" />
          <MyLink text="APP" url="/APP"></MyLink>
        </div>
      </main>
      <footer className="">
       
      </footer>
    </div>
  );
}

