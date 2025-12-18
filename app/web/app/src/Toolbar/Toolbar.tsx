import './Toolbar.css';
import React, {useEffect, useRef, useState} from 'react'
import { InputText } from 'primereact/inputtext';
import { Toolbar } from 'primereact/toolbar';
import { Calendar } from 'primereact/calendar';
import { Fieldset } from 'primereact/fieldset';
import {ru} from './ruCalendar.ts';

type DateRange = {start?: Date; end?: Date;};

interface IProps {
    updateFilter: (data: {author: string; subject: string; dateRange: DateRange}) => void;
}

export default function SearchToolbar(props: IProps) {
    const [author, setAuthor] = useState('');
    const [subject, setSubject] = useState('');
    const [dateRange, setDateRange] = useState<DateRange>({});

    const DEBOUNCE_DELAY = 1500;
    const timeoutRef = useRef();
    const isFirstRender = useRef(true);
    useEffect(() => {
        // пропускаем отправку начальных значений
        if (isFirstRender.current) {
            isFirstRender.current = false;
            return;
        }

        // Очищаем предыдущий таймер
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }
        // Устанавливаем новый таймер
        timeoutRef.current = setTimeout(() => {
            props.updateFilter({ author, subject, dateRange });
        }, DEBOUNCE_DELAY);

        // Очищаем таймер при размонтировании/смене зависимостей
        return () => clearTimeout(timeoutRef.current);
    }, [author, subject, dateRange.start, dateRange.end]);

    const startContent = (
        <InputText
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder={'Автор'}
        />
    );

    let calendarValue: [Date?, Date?] | null = null;
    if (dateRange.start && dateRange.end) {
        calendarValue = [dateRange.start, dateRange.end];
    } else if (dateRange.start) {
        calendarValue = [dateRange.start];
    } else {
        calendarValue = null;
    }

    const centerContent = (
        <Calendar<'range'>
            value={calendarValue}
            onChange={(e) => setDateRange({start: e.value[0], end: e.value[1]})}
            selectionMode="range"
            dateFormat="yy-mm-dd"
            maxDate={getMaxDate()}
            readOnlyInput
            hideOnRangeSelection
            placeholder={'Дата'}
        />

    );

    const endContent = (
        <InputText
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder={'Тематика'}
        />
    );

    return (
        <Fieldset legend="Фильтры" toggleable collapsed>
            <Toolbar start={startContent} center={centerContent} end={endContent} />
        </Fieldset>

    );
}

function getMaxDate() {
    const nowDate = new Date();
    nowDate.setDate(nowDate.getDate() + 1);
    return nowDate;
}