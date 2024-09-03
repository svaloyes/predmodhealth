import { useState } from 'react';
import { Form, Input, Button, notification } from 'antd';
import axios from 'axios';

const SurveyForm = () => {
    const [formData, setFormData] = useState({});

    const onFinish = async (values) => {
        try {
            const response = await axios.post('http://localhost:8000/', values);
            notification.success({
                message: 'Prediction',
                description: `Probability: ${response.data.prob}`,
            });
        } catch {
            notification.error({
                message: 'Error',
                description: 'There was an error with the API request.',
            });
        }
    };

    return (
        <Form onFinish={onFinish}>
            {/* Add your form fields here */}
            <Form.Item name="field1" label="Field 1">
                <Input onChange={(e) => setFormData({ ...formData, field1: e.target.value })} />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">Submit</Button>
            </Form.Item>
        </Form>
    );
};

export default SurveyForm;
