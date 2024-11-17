interface CardProps {
    title: string; 
    text: string;
  }

  function MyCard(props: CardProps) {
    return (
    <>
        <div className="flex flex-col text-white outline outline-2 outline-white mx-8 px-2 pb-4 w-1/3">
            <div className="text-[50px] mt-[15px]">
                {props.title}
            </div>
            <div className="text-[40px] mt-[15px] text-center">
                {props.text}
            </div>
        </div>
    </>
  
    )
  
  }



export default function About() {
    return (
      <div>
        <main className="flex flex-col w-full">
           <h1 className="text-[130px] mt-[15px] text-center text-white">About</h1>
            <div className="flex flex-col text-white outline outline-2 outline-white mx-8 px-2 pb-4 mb-10">
                <div className="text-[70px] mt-[15px]">
                    Our Mission
                </div>
                <div className="text-[40px] mt-[15px] text-center">
                    Mission Statement
                </div>
            </div>
            <div className="flex flex-row">
                <MyCard title="Safety" text="----" />
                <MyCard title="Efficency" text="----" />
                <MyCard title="Sustainability" text="----" />

           </div>
           
        </main>
        <footer className="">
         
        </footer>
      </div>
    );
  }
  