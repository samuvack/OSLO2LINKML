import unittest
from unittest.mock import patch

import yaml
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from linkml.validators.jsonschemavalidator import (
    JsonSchemaDataValidator,
    JsonSchemaDataValidatorError,
    _generate_jsonschema,
)
from tests.test_validation.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
DATASET_1 = env.input_path("Dataset-01.yaml")
DATASET_2 = env.input_path("Dataset-02.yaml")
PERSON_1 = env.input_path("Person-01.yaml")
PERSON_2 = env.input_path("Person-02.yaml")
PERSON_INVALID_1 = env.input_path("Person-invalid-01.yaml")


class JsonSchemaValidatorTestCase(unittest.TestCase):
    def setUp(self):
        # Ensure each test runs from a clean state
        _generate_jsonschema.cache_clear()

    def test_validate_object(self):
        mod = PythonGenerator(SCHEMA).compile_module()
        validator = JsonSchemaDataValidator(schema=SCHEMA)

        obj = yaml_loader.load(source=PERSON_1, target_class=mod.Person)
        result = validator.validate_object(obj, target_class=mod.Person)
        self.assertIsNone(result)

        with self.assertRaises(JsonSchemaDataValidatorError) as ctx:
            obj = yaml_loader.load(source=PERSON_INVALID_1, target_class=mod.Person)
            validator.validate_object(obj, target_class=mod.Person)

        messages = ctx.exception.validation_messages
        self.assertEqual(len(messages), 1)
        self.assertIn("name", messages[0])

    def test_validate_dict(self):
        validator = JsonSchemaDataValidator(schema=SCHEMA)

        with open(PERSON_1) as file:
            obj = yaml.safe_load(file)
        result = validator.validate_dict(obj, "Person")
        self.assertIsNone(result)

        with open(PERSON_2) as file:
            obj = yaml.safe_load(file)

        with self.assertRaises(JsonSchemaDataValidatorError) as ctx:
            validator.validate_dict(obj, "Person")

        with open(PERSON_INVALID_1) as file:
            obj = yaml.safe_load(file)

        with self.assertRaises(JsonSchemaDataValidatorError) as ctx:
            validator.validate_dict(obj, "Person")

        messages = ctx.exception.validation_messages
        self.assertEqual(len(messages), 1)
        self.assertIn("name", messages[0])

    def test_validate_dict_including_descendants(self):
        validator = JsonSchemaDataValidator(schema=SCHEMA, include_range_class_descendants=True)

        with open(PERSON_1) as file:
            obj = yaml.safe_load(file)
        result = validator.validate_dict(obj, "Person")
        self.assertIsNone(result)

        with open(PERSON_2) as file:
            obj = yaml.safe_load(file)
        result = validator.validate_dict(obj, "Person")
        self.assertIsNone(result)

        with open(PERSON_INVALID_1) as file:
            obj = yaml.safe_load(file)

        with self.assertRaises(JsonSchemaDataValidatorError) as ctx:
            validator.validate_dict(obj, "Person")

        messages = ctx.exception.validation_messages
        self.assertEqual(len(messages), 1)
        self.assertIn("name", messages[0])

    @patch("linkml.generators.jsonschemagen.JsonSchemaGenerator.generate", return_value={})
    def test_jsonschema_caching(self, generate_mock):
        """Validate that JSON Schema generation is only done when needed"""

        mod = PythonGenerator(SCHEMA).compile_module()
        v = JsonSchemaDataValidator(schema=SCHEMA)

        # Validate against the Dataset class for the first time. This should
        # result in the JsonSchemaGenerator.generate being called once
        obj = yaml_loader.load(source=DATASET_1, target_class=mod.Dataset)
        v.validate_object(obj, target_class=mod.Dataset)
        generate_mock.assert_called_once()

        # Validate against the Dataset class for a second time. The JSON Schema
        # generated by the previous validate_object call should have been cached.
        # Verify that JsonSchemaGenerator.generate was not called again.
        generate_mock.reset_mock()
        obj = yaml_loader.load(source=DATASET_2, target_class=mod.Dataset)
        v.validate_object(obj, target_class=mod.Dataset)
        generate_mock.assert_not_called()

        # Validate against a different class in the schema, Person. This should
        # result in an additional call to JsonSchemaGenerator.generate.
        generate_mock.reset_mock()
        obj = yaml_loader.load(source=PERSON_1, target_class=mod.Person)
        v.validate_object(obj, target_class=mod.Person)
        generate_mock.called_once()


if __name__ == "__main__":
    unittest.main()