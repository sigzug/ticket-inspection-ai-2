import {Container} from "@chakra-ui/react";
import Nav from "./components/Nav";
import Dashboard from "./pages/Dashboard";

export default function App() {
    return (
        <Container p={0} m={0} h={"100vh"} w={"100%"}>
            <Nav/>
            <Dashboard/>
        </Container>
    );
}
