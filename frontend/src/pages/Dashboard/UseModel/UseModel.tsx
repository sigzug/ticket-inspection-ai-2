import {useState} from "react";
import axios from "axios";
import {Box, Button, Card, Field, Input, Stack, Text,} from "@chakra-ui/react";

interface UseModelRequest {
    line: string;
    departure_station: string;
    arrival_station: string;
    only_standing: boolean;
    departure_time: Date;
}

export const UseModel = () => {
    const [form, setForm] = useState<UseModelRequest>({
        line: "",
        departure_station: "",
        arrival_station: "",
        only_standing: false,
        departure_time: new Date(),
    });
    const [response, setResponse] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (key: string, value: string) => {
        setForm((prev) => ({...prev, [key]: value}));
    };

    const handleSubmit = async () => {
        try {
            setLoading(true);
            setResponse(null);

            const res = await axios.post("http://localhost:8000/api/use-model/", {
                ...form,
                only_standing: form.only_standing,
                departure_time: new Date(form.departure_time).toISOString(),
            });

            setResponse(res.data);
        } catch (err: any) {
            setResponse({error: err.message});
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card.Root maxW="sm" shadow="sm" borderWidth="md">
            <Card.Header>
                <Card.Title>Use the model</Card.Title>
                <Card.Description>
                    Fill in details about your planned trip and the model will make a prediction.
                </Card.Description>
            </Card.Header>

            <Card.Body>
                <Stack gap="4" w="full">
                    <Field.Root>
                        <Field.Label>Line</Field.Label>
                        <Input
                            value={form.line}
                            onChange={(e) => handleChange("line", e.target.value)}
                        />
                    </Field.Root>

                    <Field.Root>
                        <Field.Label>Departure station</Field.Label>
                        <Input
                            value={form.departure_station}
                            onChange={(e) => handleChange("departure_station", e.target.value)}
                        />
                    </Field.Root>

                    <Field.Root>
                        <Field.Label>Arrival station</Field.Label>
                        <Input
                            value={form.arrival_station}
                            onChange={(e) => handleChange("arrival_station", e.target.value)}
                        />
                    </Field.Root>

                    <Field.Root>
                        <Field.Label>Only standing (true/false)</Field.Label>
                        <Input
                            value={form.only_standing}
                            onChange={(e) => handleChange("only_standing", e.target.value)}
                        />
                    </Field.Root>

                    <Field.Root>
                        <Field.Label>Departure time</Field.Label>
                        <Input
                            type="datetime-local"
                            value={form.departure_time}
                            onChange={(e) => handleChange("departure_time", e.target.value)}
                        />
                    </Field.Root>
                </Stack>
            </Card.Body>

            <Card.Footer justifyContent="flex-end" gap="3">
                <Button variant="outline" onClick={() => setForm({
                    line: "",
                    departure_station: "",
                    arrival_station: "",
                    only_standing: "",
                    departure_time: "",
                })}>
                    Reset
                </Button>
                <Button variant="solid" onClick={handleSubmit} loading={loading}>
                    Submit
                </Button>
            </Card.Footer>

            {response && (
                <Box borderTopWidth="1px" p="4">
                    <Text fontWeight="bold" mb="2">
                        Response:
                    </Text>
                    <Box
                        bg="bg.muted"
                        p="3"
                        borderRadius="md"
                        fontSize="sm"
                        whiteSpace="pre-wrap"
                    >
                        {JSON.stringify(response, null, 2)}
                    </Box>
                </Box>
            )}
        </Card.Root>
    );
};
