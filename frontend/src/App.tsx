import {Button, Heading, Text, Card} from "@chakra-ui/react";

export default function App() {
    return (
        <Card.Root size="lg" variant="elevated" p="6">
            <Card.Body>
                <Heading mb="4">Chakra v3 ✅</Heading>
                <Text mb="4">Card bruker slots i v3.</Text>
                <Button colorPalette="blue">Klikk meg</Button>
            </Card.Body>
        </Card.Root>
    );
}
