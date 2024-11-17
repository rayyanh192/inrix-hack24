import Image from "next/image";

export default function Home() {
  return (
    <div>
      <main className="w-full">
          <div className="text-white font-serif	text-center">
          <div className="text-[65px] mt-[100px]">WELCOME TO</div>
          <h1 className="text-[175px] mt-[15px]">EmergenSee</h1>
          <div className="text-[90px] mt-[15px] italic">Safety in Sight</div>
        </div>
        <div className="flex flex-col items-center mt-[30px]">
          <button className="text-[40px] text-black font-serif text-center mt-[30px] bg-white p-[6px] w-[200px] border-[2px] border-black">
            <a href="/ABOUT">ABOUT</a>
          </button>
          <button className="text-[40px] text-black font-serif text-center mt-[30px] bg-white p-[6px] w-[200px] border-[2px] border-black">
            <a href="/APP">APP</a>
          </button>
        </div>
      </main>
      <footer className="">
       
      </footer>
    </div>
  );
}
