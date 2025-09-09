import {Button, Card, Field, Input, Stack} from "@chakra-ui/react";

export const UseModel = () => {
    return (
        <Card.Root maxW="sm" shadow="sm" borderWidth="md">
            <Card.Header>
                <Card.Title>Use the model</Card.Title>
                <Card.Description>
                    Fill in details about your planned trip and the model will give a guess about ticket inspection.
                </Card.Description>
            </Card.Header>
            <Card.Body>
                <Stack gap="4" w="full">
                    <Field.Root>
                        <Field.Label>First Name</Field.Label>
                        <Input/>
                    </Field.Root>
                    <Field.Root>
                        <Field.Label>Last Name</Field.Label>
                        <Input/>
                    </Field.Root>
                </Stack>
            </Card.Body>
            <Card.Footer justifyContent="flex-end">
                <Button variant="outline">Cancel</Button>
                <Button variant="solid">Sign in</Button>
            </Card.Footer>
        </Card.Root>
    )
}