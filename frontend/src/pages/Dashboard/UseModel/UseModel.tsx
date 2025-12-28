import { useState } from "react";
import { Box, Button, Card, Field, Input, Stack, Text, NativeSelect } from "@chakra-ui/react";
import { useCategories } from "../../../hooks/useCategories";
import { useRunModel } from "../../../hooks/useRunModel";
import type { UseModelRequest } from "../../../interfaces";

export const UseModel = () => {
  const [form, setForm] = useState<UseModelRequest>({
    line: "",
    departure_station: "",
    arrival_station: "",
    only_standing: false,
    departure_time: new Date(),
  });

  const { categories, isLoading, isError } = useCategories();
  const {
    runModel,
    data: response,
    error: submitError,
    isMutating,
    reset: resetMutation,
  } = useRunModel();

  const lineOptions = categories?.line ?? [];
  const departureOptions = categories?.departure_station ?? [];
  const arrivalOptions = categories?.arrival_station ?? [];

  const handleChange = (key: keyof UseModelRequest, value: any) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async () => {
    await runModel({
      ...form,
      // departure_time is converted to ISO in the hook
    });
  };

  const handleReset = () => {
    setForm({
      line: "",
      departure_station: "",
      arrival_station: "",
      only_standing: false,
      departure_time: "" as any,
    });
    resetMutation();
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
            <NativeSelect.Root
              value={form.line}
              onChange={(e) => handleChange("line", e.target.value)}
              disabled={isLoading || isError || lineOptions.length === 0}
            >
              <NativeSelect.Field>
                <option value="" disabled>
                  {isLoading ? "Loading..." : "Select line"}
                </option>
                {lineOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </NativeSelect.Field>
              <NativeSelect.Indicator />
            </NativeSelect.Root>
          </Field.Root>

          <Field.Root>
            <Field.Label>Departure station</Field.Label>
            <NativeSelect.Root
              value={form.departure_station}
              onChange={(e) => handleChange("departure_station", e.target.value)}
              disabled={isLoading || isError || departureOptions.length === 0}
            >
              <NativeSelect.Field>
                <option value="" disabled>
                  {isLoading ? "Loading..." : "Select departure station"}
                </option>
                {departureOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </NativeSelect.Field>
              <NativeSelect.Indicator />
            </NativeSelect.Root>
          </Field.Root>

          <Field.Root>
            <Field.Label>Arrival station</Field.Label>
            <NativeSelect.Root
              value={form.arrival_station}
              onChange={(e) => handleChange("arrival_station", e.target.value)}
              disabled={isLoading || isError || arrivalOptions.length === 0}
            >
              <NativeSelect.Field>
                <option value="" disabled>
                  {isLoading ? "Loading..." : "Select arrival station"}
                </option>
                {arrivalOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </NativeSelect.Field>
              <NativeSelect.Indicator />
            </NativeSelect.Root>
          </Field.Root>

          <Field.Root>
            <Field.Label>Only standing (true/false)</Field.Label>
            <Input
              value={form.only_standing as any}
              onChange={(e) => handleChange("only_standing", e.target.value)}
            />
          </Field.Root>

          <Field.Root>
            <Field.Label>Departure time</Field.Label>
            <Input
              type="datetime-local"
              value={form.departure_time as any}
              onChange={(e) => handleChange("departure_time", e.target.value)}
            />
          </Field.Root>

          {isError && (
            <Box color="red.500" fontSize="sm">
              Failed to load categories. Please try again.
            </Box>
          )}
        </Stack>
      </Card.Body>

      <Card.Footer justifyContent="flex-end" gap="3">
        <Button variant="outline" onClick={handleReset}>
          Reset
        </Button>
        <Button variant="solid" onClick={handleSubmit} loading={isMutating}>
          Submit
        </Button>
      </Card.Footer>

      {(submitError || response) && (
        <Box borderTopWidth="1px" p="4">
          <Text fontWeight="bold" mb="2">
            Response:
          </Text>
          <Box bg="bg.muted" p="3" borderRadius="md" fontSize="sm" whiteSpace="pre-wrap">
            {submitError
              ? JSON.stringify({ error: (submitError as any)?.message ?? "Submit failed" }, null, 2)
              : JSON.stringify(response, null, 2)}
          </Box>
        </Box>
      )}
    </Card.Root>
  );
};
