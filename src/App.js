import "./App.css";
import Papa from "papaparse";
import { useEffect, useState } from "react";

function App() {
  const [read, setRead] = useState({ data: [] });
  useEffect(() => {
      Papa.parse("./save.csv", {
        header: true,
        delimiter: ",",
        download: true,
        skipEmptyLines: true,
        complete: (res) => {
          let sortFunc = (a, b) => {
            let day1 = new Date(a.Added.split(" ")[1]);
            let day2 = new Date(b.Added.split(" ")[1]);
            if (day1 === day2) {
              return 0;
            } else {
              return day1 < day2 ? 1 : -1;
            }
          };
          let reader = res.data.sort(sortFunc);
          setRead({ data: reader });
        },
      });
    const interval = setInterval(() => {
      Papa.parse("./save.csv", {
        header: true,
        delimiter: ",",
        download: true,
        skipEmptyLines: true,
        complete: (res) => {
          let sortFunc = (a, b) => {
            let day1 = new Date(a.Added.split(" ")[1]);
            let day2 = new Date(b.Added.split(" ")[1]);
            if (day1 === day2) {
              return 0;
            } else {
              return day1 < day2 ? 1 : -1;
            }
          };
          let reader = res.data.sort(sortFunc);
          setRead({ data: reader });
        },
      });
    }, 60000);
    return () => clearInterval(interval);
  });

  return (
    <div className="App">
      <table
        class="table table-striped table-hover table-sm"
        style={{ fontFamily: "Open Sans" }}
      >
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Available</th>
            <th>Link</th>
            <th>Added From</th>
            <th>Image</th>
          </tr>
        </thead>

        <tbody style={{ textAlign: "center", verticalAlign: "middle" }}>
          {read.data.map((i) => {
            return (
              <>
                <tr
                  key={i.Link}
                  class={
                    i.Req !== ""
                      ? i.Req === "TRUE"
                        ? "table-success"
                        : "table-danger"
                      : ""
                  }
                >
                  <td>
                    {i.Street} {i.Area}
                  </td>
                  <td>{i.Price}</td>
                  <td>{i.Available}</td>
                  <td>
                    <a href={i.Link}>{i.Link}</a>
                  </td>
                  <td>{i.Added}</td>
                  <td>
                    <img width={150} height={100} src={i.Image} alt="home" />
                  </td>
                </tr>
              </>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default App;
