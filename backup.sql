PGDMP  7    8                |         
   Integrador    16.3    16.3     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16411 
   Integrador    DATABASE     �   CREATE DATABASE "Integrador" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Argentina.1252';
    DROP DATABASE "Integrador";
                postgres    false            �            1259    16428    torneos    TABLE     �   CREATE TABLE public.torneos (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    fecha date NOT NULL,
    lugar character varying(100) NOT NULL
);
    DROP TABLE public.torneos;
       public         heap    postgres    false            �            1259    16427    torneos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.torneos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.torneos_id_seq;
       public          postgres    false    218            �           0    0    torneos_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.torneos_id_seq OWNED BY public.torneos.id;
          public          postgres    false    217            �            1259    16435    user_tournaments    TABLE     h   CREATE TABLE public.user_tournaments (
    user_id integer NOT NULL,
    torneos_id integer NOT NULL
);
 $   DROP TABLE public.user_tournaments;
       public         heap    postgres    false            �            1259    16413    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16412    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    216                        0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    215            Z           2604    16431 
   torneos id    DEFAULT     h   ALTER TABLE ONLY public.torneos ALTER COLUMN id SET DEFAULT nextval('public.torneos_id_seq'::regclass);
 9   ALTER TABLE public.torneos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            Y           2604    16416    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            �          0    16428    torneos 
   TABLE DATA           ;   COPY public.torneos (id, nombre, fecha, lugar) FROM stdin;
    public          postgres    false    218   �       �          0    16435    user_tournaments 
   TABLE DATA           ?   COPY public.user_tournaments (user_id, torneos_id) FROM stdin;
    public          postgres    false    219   �       �          0    16413    users 
   TABLE DATA           >   COPY public.users (id, username, email, password) FROM stdin;
    public          postgres    false    216   �                  0    0    torneos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.torneos_id_seq', 8, true);
          public          postgres    false    217                       0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 29, true);
          public          postgres    false    215            `           2606    16433    torneos torneos_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.torneos
    ADD CONSTRAINT torneos_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.torneos DROP CONSTRAINT torneos_pkey;
       public            postgres    false    218            b           2606    16439 &   user_tournaments user_tournaments_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY public.user_tournaments
    ADD CONSTRAINT user_tournaments_pkey PRIMARY KEY (user_id, torneos_id);
 P   ALTER TABLE ONLY public.user_tournaments DROP CONSTRAINT user_tournaments_pkey;
       public            postgres    false    219    219            \           2606    16420    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false    216            ^           2606    16418    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            c           2606    16445 1   user_tournaments user_tournaments_torneos_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_tournaments
    ADD CONSTRAINT user_tournaments_torneos_id_fkey FOREIGN KEY (torneos_id) REFERENCES public.torneos(id);
 [   ALTER TABLE ONLY public.user_tournaments DROP CONSTRAINT user_tournaments_torneos_id_fkey;
       public          postgres    false    219    218    4704            d           2606    16440 .   user_tournaments user_tournaments_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_tournaments
    ADD CONSTRAINT user_tournaments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 X   ALTER TABLE ONLY public.user_tournaments DROP CONSTRAINT user_tournaments_user_id_fkey;
       public          postgres    false    219    4702    216            �   �   x�]�A
�0 ϻ��"iڪ�V(zQ��K�k	�]Hҋ�����yf`
��c��N�ƙzkl��N5�3�D��@-d�DA]S�eњ��A�g,��^���p&����NBb�ֺ4����FY��{m����T�\�ǥ��-��D� �j<�      �   >   x�%��� �7WL_��^���3Z�,�j�X��A��!�Z�Ie�Ԥ~��	��#� ���      �   �   x�e��� ���a?:'�=�.l���?!��~�7��M�5)i����%���������Ru#�D�K��+���o�����} :�X�T���@��G�3�,e��5�'K�ew�7T#�m�������p��
�]	!�o�K%     